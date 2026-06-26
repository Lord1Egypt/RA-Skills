package zoho

import (
	"bytes"
	"context"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"net/url"
	"strconv"
	"strings"

	"golang.org/x/oauth2"
)

const apiBase = "https://mail.zoho.eu/api"

// Client provides access to the Zoho Mail REST API.
type Client struct {
	http      *http.Client
	email     string
	accountID string // cached after first discovery
}

// NewClient creates a Zoho Mail API client using the provided token source.
// email is the configured mailbox address (used to identify the account).
func NewClient(ctx context.Context, ts oauth2.TokenSource, email string) *Client {
	return &Client{
		http:  oauth2.NewClient(ctx, ts),
		email: email,
	}
}

// apiResponse is the envelope returned by the Zoho Mail API.
type apiResponse struct {
	Status struct {
		Code        int    `json:"code"`
		Description string `json:"description"`
	} `json:"status"`
	Data json.RawMessage `json:"data"`
}

func (c *Client) do(req *http.Request) (*apiResponse, error) {
	resp, err := c.http.Do(req)
	if err != nil {
		return nil, fmt.Errorf("http request: %w", err)
	}
	defer func() { _ = resp.Body.Close() }()

	body, err := io.ReadAll(resp.Body)
	if err != nil {
		return nil, fmt.Errorf("reading response body: %w", err)
	}

	if resp.StatusCode == http.StatusNoContent {
		return &apiResponse{}, nil
	}

	var ar apiResponse
	if err := json.Unmarshal(body, &ar); err != nil {
		return nil, fmt.Errorf("parsing response (status %d): %w", resp.StatusCode, err)
	}

	if ar.Status.Code != 200 {
		return nil, fmt.Errorf("zoho api error %d: %s", ar.Status.Code, ar.Status.Description)
	}

	return &ar, nil
}

func (c *Client) get(ctx context.Context, path string, params url.Values) (*apiResponse, error) {
	u := apiBase + path
	if len(params) > 0 {
		u += "?" + params.Encode()
	}

	req, err := http.NewRequestWithContext(ctx, http.MethodGet, u, nil)
	if err != nil {
		return nil, fmt.Errorf("building request: %w", err)
	}

	return c.do(req)
}

func (c *Client) post(ctx context.Context, path string, body any) (*apiResponse, error) {
	data, err := json.Marshal(body)
	if err != nil {
		return nil, fmt.Errorf("marshalling request: %w", err)
	}

	req, err := http.NewRequestWithContext(ctx, http.MethodPost, apiBase+path, bytes.NewReader(data))
	if err != nil {
		return nil, fmt.Errorf("building request: %w", err)
	}
	req.Header.Set("Content-Type", "application/json")

	return c.do(req)
}

func (c *Client) put(ctx context.Context, path string, body any) (*apiResponse, error) {
	data, err := json.Marshal(body)
	if err != nil {
		return nil, fmt.Errorf("marshalling request: %w", err)
	}

	req, err := http.NewRequestWithContext(ctx, http.MethodPut, apiBase+path, bytes.NewReader(data))
	if err != nil {
		return nil, fmt.Errorf("building request: %w", err)
	}
	req.Header.Set("Content-Type", "application/json")

	return c.do(req)
}

func (c *Client) delete(ctx context.Context, path string, params url.Values) (*apiResponse, error) {
	u := apiBase + path
	if len(params) > 0 {
		u += "?" + params.Encode()
	}

	req, err := http.NewRequestWithContext(ctx, http.MethodDelete, u, nil)
	if err != nil {
		return nil, fmt.Errorf("building request: %w", err)
	}

	return c.do(req)
}

// accountEntry is the shape returned by GET /accounts.
type accountEntry struct {
	AccountID    string `json:"accountId"`
	EmailAddress string `json:"emailAddress"`
}

// AccountID returns the Zoho account ID for the configured email address,
// fetching it from the API on first call and caching it thereafter.
func (c *Client) AccountID(ctx context.Context) (string, error) {
	if c.accountID != "" {
		return c.accountID, nil
	}

	ar, err := c.get(ctx, "/accounts", nil)
	if err != nil {
		return "", fmt.Errorf("listing accounts: %w", err)
	}

	var accounts []accountEntry
	if err := json.Unmarshal(ar.Data, &accounts); err != nil {
		return "", fmt.Errorf("parsing accounts: %w", err)
	}

	for _, a := range accounts {
		if strings.EqualFold(a.EmailAddress, c.email) {
			c.accountID = a.AccountID
			return c.accountID, nil
		}
	}

	return "", fmt.Errorf("no account found for email %q; check 'zoho-mail config show'", c.email)
}

// Message is a summary of a Zoho mail message.
type Message struct {
	MessageID    string `json:"messageId"`
	Subject      string `json:"subject"`
	FromAddress  string `json:"fromAddress"`
	ToAddress    string `json:"toAddress"`
	ReceivedTime string `json:"receivedTime"`
	FolderID     string `json:"folderId"`
	IsRead       bool   `json:"isRead"`
	Summary      string `json:"summary"`
}

// MessageDetail is a full message with content.
type MessageDetail struct {
	Message
	Content     string `json:"content"`
	HTMLContent string `json:"htmlContent"`
}

// SendRequest contains the fields needed to send or reply to a message.
type SendRequest struct {
	FromAddress string `json:"fromAddress"`
	ToAddress   string `json:"toAddress"`
	CCAddress   string `json:"ccAddress,omitempty"`
	Subject     string `json:"subject"`
	Content     string `json:"content"`
	MailFormat  string `json:"mailFormat"` // "html" or "plaintext"
	InReplyTo   string `json:"inReplyTo,omitempty"`
}

// Folder represents a Zoho Mail folder.
type Folder struct {
	FolderID     string `json:"folderId"`
	FolderName   string `json:"folderName"`
	FolderType   string `json:"folderType"`
	MessageCount int    `json:"messageCount"`
	UnreadCount  int    `json:"unreadCount"`
}

// ListMessages returns messages in the given folder (pass empty string for INBOX).
func (c *Client) ListMessages(ctx context.Context, folderID string, limit, start int) ([]Message, error) {
	accountID, err := c.AccountID(ctx)
	if err != nil {
		return nil, err
	}

	params := url.Values{
		"limit": {strconv.Itoa(limit)},
		"start": {strconv.Itoa(start)},
	}
	if folderID != "" {
		params.Set("folderId", folderID)
	}

	ar, err := c.get(ctx, fmt.Sprintf("/accounts/%s/messages/view", accountID), params)
	if err != nil {
		return nil, fmt.Errorf("listing messages: %w", err)
	}

	var messages []Message
	if err := json.Unmarshal(ar.Data, &messages); err != nil {
		return nil, fmt.Errorf("parsing messages: %w", err)
	}

	return messages, nil
}

// GetMessage returns the full content of a message by ID.
func (c *Client) GetMessage(ctx context.Context, msgID string) (MessageDetail, error) {
	accountID, err := c.AccountID(ctx)
	if err != nil {
		return MessageDetail{}, err
	}

	ar, err := c.get(ctx, fmt.Sprintf("/accounts/%s/messages/%s", accountID, msgID), nil)
	if err != nil {
		return MessageDetail{}, fmt.Errorf("getting message %s: %w", msgID, err)
	}

	var msg MessageDetail
	if err := json.Unmarshal(ar.Data, &msg); err != nil {
		return MessageDetail{}, fmt.Errorf("parsing message: %w", err)
	}

	return msg, nil
}

// SendMessage sends a new message or reply.
func (c *Client) SendMessage(ctx context.Context, req SendRequest) (Message, error) {
	accountID, err := c.AccountID(ctx)
	if err != nil {
		return Message{}, err
	}

	if req.MailFormat == "" {
		req.MailFormat = "plaintext"
	}

	ar, err := c.post(ctx, fmt.Sprintf("/accounts/%s/messages", accountID), req)
	if err != nil {
		return Message{}, fmt.Errorf("sending message: %w", err)
	}

	var sent Message
	if err := json.Unmarshal(ar.Data, &sent); err != nil {
		return Message{}, fmt.Errorf("parsing send response: %w", err)
	}

	return sent, nil
}

// DeleteMessage deletes a message.
func (c *Client) DeleteMessage(ctx context.Context, msgID, folderID string) error {
	accountID, err := c.AccountID(ctx)
	if err != nil {
		return err
	}

	params := url.Values{}
	if folderID != "" {
		params.Set("folderId", folderID)
	}

	_, err = c.delete(ctx, fmt.Sprintf("/accounts/%s/messages/%s", accountID, msgID), params)
	if err != nil {
		return fmt.Errorf("deleting message %s: %w", msgID, err)
	}

	return nil
}

// MarkRead marks the given message IDs as read or unread.
func (c *Client) MarkRead(ctx context.Context, msgIDs []string, isRead bool) error {
	accountID, err := c.AccountID(ctx)
	if err != nil {
		return err
	}

	body := map[string]any{
		"messageId": msgIDs,
		"isRead":    isRead,
	}

	_, err = c.put(ctx, fmt.Sprintf("/accounts/%s/messages", accountID), body)
	if err != nil {
		return fmt.Errorf("marking messages: %w", err)
	}

	return nil
}

// SearchMessages searches for messages matching the query.
func (c *Client) SearchMessages(ctx context.Context, query string, limit int) ([]Message, error) {
	accountID, err := c.AccountID(ctx)
	if err != nil {
		return nil, err
	}

	params := url.Values{
		"searchKey":   {query},
		"searchLimit": {strconv.Itoa(limit)},
	}

	ar, err := c.get(ctx, fmt.Sprintf("/accounts/%s/messages/search", accountID), params)
	if err != nil {
		return nil, fmt.Errorf("searching messages: %w", err)
	}

	var messages []Message
	if err := json.Unmarshal(ar.Data, &messages); err != nil {
		return nil, fmt.Errorf("parsing search results: %w", err)
	}

	return messages, nil
}

// ListFolders returns all folders for the account.
func (c *Client) ListFolders(ctx context.Context) ([]Folder, error) {
	accountID, err := c.AccountID(ctx)
	if err != nil {
		return nil, err
	}

	ar, err := c.get(ctx, fmt.Sprintf("/accounts/%s/folders", accountID), nil)
	if err != nil {
		return nil, fmt.Errorf("listing folders: %w", err)
	}

	var folders []Folder
	if err := json.Unmarshal(ar.Data, &folders); err != nil {
		return nil, fmt.Errorf("parsing folders: %w", err)
	}

	return folders, nil
}
