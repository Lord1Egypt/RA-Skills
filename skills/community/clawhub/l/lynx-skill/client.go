package main

import (
	"bytes"
	"encoding/base64"
	"encoding/json"
	"fmt"
	"io"
	"mime/multipart"
	"net/http"
	"net/http/cookiejar"
	"os"
	"strings"
	"time"

	"dodmcdund.cc/lynx-travel-agent/lynxskill/gwt"
)

type LynxClient struct {
	config    *Config
	client    *http.Client
	jsession  string
	expiresAt time.Time
}

func NewLynxClient(cfg *Config) *LynxClient {
	jar, _ := cookiejar.New(nil)
	return &LynxClient{
		config: cfg,
		client: &http.Client{Jar: jar, Timeout: 30 * time.Second},
	}
}

func (c *LynxClient) ensureSession() error {
	if c.jsession != "" && time.Now().Before(c.expiresAt) {
		return nil
	}

	body := gwt.BuildLoginBody(c.config.RemoteHost, c.config.CompanyCode, c.config.Username, c.config.Password)
	req, err := http.NewRequest("POST", fmt.Sprintf("https://%s/lynx/service/security.rpc", c.config.RemoteHost), strings.NewReader(body))
	if err != nil {
		return fmt.Errorf("failed to create auth request: %w", err)
	}
	req.Header.Set("Content-Type", gwt.ContentType)
	req.Header.Set("Accept", gwt.ContentType)

	resp, err := c.client.Do(req)
	if err != nil {
		return fmt.Errorf("failed to perform auth request: %w", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		respBody, _ := io.ReadAll(resp.Body)
		return fmt.Errorf("auth request failed with status %d: %s", resp.StatusCode, string(respBody))
	}

	respBody, err := io.ReadAll(resp.Body)
	if err != nil {
		return fmt.Errorf("failed to read auth response body: %w", err)
	}

	bodyStr := string(respBody)
	if strings.HasPrefix(bodyStr, "//EX") {
		errMsg, parseErr := gwt.ParseErrorResponse(bodyStr)
		if parseErr == nil {
			return fmt.Errorf("auth failed: %s", errMsg)
		}
		return fmt.Errorf("auth failed: %s", bodyStr)
	}
	if !strings.HasPrefix(bodyStr, "//OK") {
		return fmt.Errorf("unexpected auth response: %s", bodyStr)
	}

	for _, cookie := range resp.Cookies() {
		if cookie.Name == "JSESSIONID" {
			c.jsession = cookie.Value
			c.expiresAt = time.Now().Add(15 * time.Minute)
			return nil
		}
	}

	return fmt.Errorf("JSESSIONID not found in response cookies")
}

func (c *LynxClient) postGWT(url, body string) (string, error) {
	if err := c.ensureSession(); err != nil {
		return "", err
	}

	req, err := http.NewRequest("POST", fmt.Sprintf("https://%s%s", c.config.RemoteHost, url), strings.NewReader(body))
	if err != nil {
		return "", fmt.Errorf("failed to create request: %w", err)
	}
	req.Header.Set("Content-Type", gwt.ContentType)
	req.AddCookie(&http.Cookie{
		Name:   "JSESSIONID",
		Value:  c.jsession,
		Domain: c.config.RemoteHost,
		Path:   "/lynx",
	})

	resp, err := c.client.Do(req)
	if err != nil {
		return "", fmt.Errorf("failed to execute request: %w", err)
	}
	defer resp.Body.Close()

	respBody, err := io.ReadAll(resp.Body)
	if err != nil {
		return "", fmt.Errorf("failed to read response body: %w", err)
	}
	bodyStr := string(respBody)

	if resp.StatusCode == http.StatusOK && strings.HasPrefix(bodyStr, "//EX") {
		errMsg, parseErr := gwt.ParseErrorResponse(bodyStr)
		if parseErr == nil {
			return "", fmt.Errorf("GWT error: %s", errMsg)
		}
		return "", fmt.Errorf("GWT error: %s", bodyStr)
	}

	return bodyStr, nil
}

func (c *LynxClient) uploadAttachment(binaryBase64, identifier, fileName string) (string, error) {
	if err := c.ensureSession(); err != nil {
		return "", err
	}

	var requestBody bytes.Buffer
	writer := multipart.NewWriter(&requestBody)

	fileIdField, _ := writer.CreateFormField("fileId")
	fileIdField.Write([]byte(identifier))

	fileData, err := base64.StdEncoding.DecodeString(binaryBase64)
	if err != nil {
		return "", fmt.Errorf("failed to decode base64 data: %w", err)
	}

	fileField, _ := writer.CreateFormFile("file", fileName)
	fileField.Write(fileData)
	writer.Close()

	req, err := http.NewRequest("POST", fmt.Sprintf("https://%s/lynx/fileDocumentUpload", c.config.RemoteHost), &requestBody)
	if err != nil {
		return "", fmt.Errorf("failed to create attachment upload request: %w", err)
	}
	req.Header.Set("Content-Type", writer.FormDataContentType())
	req.AddCookie(&http.Cookie{
		Name:   "JSESSIONID",
		Value:  c.jsession,
		Domain: c.config.RemoteHost,
		Path:   "/lynx",
	})

	resp, err := c.client.Do(req)
	if err != nil {
		return "", fmt.Errorf("failed to execute attachment upload request: %w", err)
	}
	defer resp.Body.Close()

	bodyBytes, _ := io.ReadAll(resp.Body)
	bodyStr := string(bodyBytes)

	if resp.StatusCode != http.StatusOK {
		return "", fmt.Errorf("attachment upload failed with status %d: %s", resp.StatusCode, bodyStr)
	}

	attachmentUrl, err := parseAttachmentUploadResponse(bodyStr)
	if err != nil {
		return "", fmt.Errorf("invalid attachment upload response: %w", err)
	}

	return attachmentUrl, nil
}

func parseAttachmentUploadResponse(responseBody string) (string, error) {
	if !strings.HasPrefix(responseBody, "SUCCESS:") {
		return "", fmt.Errorf("unexpected response format: %s", responseBody)
	}
	urlPart := strings.TrimPrefix(responseBody, "SUCCESS:")
	urlPart = strings.TrimSpace(urlPart)
	if !strings.HasSuffix(urlPart, ":") {
		return "", fmt.Errorf("response does not end with ':': %s", responseBody)
	}
	urlPart = strings.TrimSuffix(urlPart, ":")
	if urlPart == "" || !strings.HasPrefix(urlPart, "/") {
		return "", fmt.Errorf("invalid attachment URL in response: %s", responseBody)
	}
	return urlPart, nil
}

func (c *LynxClient) FileSearchByPartyName(partyName string) (*gwt.FileSearchResponse, error) {
	body := gwt.BuildFileSearchByPartyNameBody(c.config.RemoteHost, partyName)
	respBody, err := c.postGWT("/lynx/service/file.rpc", body)
	if err != nil {
		return nil, fmt.Errorf("file search by party name failed: %w", err)
	}
	return gwt.ParseFileSearchResponse(respBody)
}

func (c *LynxClient) FileSearchByFileReference(fileReference string) (*gwt.FileSearchResponse, error) {
	body := gwt.BuildFileSearchByFileReferenceBody(c.config.RemoteHost, fileReference)
	respBody, err := c.postGWT("/lynx/service/file.rpc", body)
	if err != nil {
		return nil, fmt.Errorf("file search by file reference failed: %w", err)
	}
	return gwt.ParseFileSearchResponse(respBody)
}

func (c *LynxClient) RetrieveItinerary(fileIdentifier string, showCancelled bool) (*gwt.ItineraryResponse, error) {
	body := gwt.BuildRetrieveItineraryBody(c.config.RemoteHost, fileIdentifier, showCancelled)
	respBody, err := c.postGWT("/lynx/service/file.rpc", body)
	if err != nil {
		return nil, fmt.Errorf("retrieve itinerary failed: %w", err)
	}
	if os.Getenv("LYNX_DEBUG") != "" {
		safe := strings.NewReplacer("$", "_", "/", "_").Replace(fileIdentifier)
		os.WriteFile(fmt.Sprintf("/tmp/itinerary_raw_%s.txt", safe), []byte(respBody), 0644)
	}
	return gwt.ParseRetrieveItineraryResponse(respBody)
}

func (c *LynxClient) RetrieveFileDocuments(fileIdentifier, transactionIdentifier string) (*gwt.FileDocumentsResponse, error) {
	var body string
	if transactionIdentifier == "" {
		body = gwt.BuildFileDocumentsByFileReferenceBody(c.config.RemoteHost, fileIdentifier)
	} else {
		body = gwt.BuildFileDocumentsByTransactionReferenceBody(c.config.RemoteHost, fileIdentifier, transactionIdentifier)
	}
	respBody, err := c.postGWT("/lynx/service/file.rpc", body)
	if err != nil {
		return nil, fmt.Errorf("retrieve file documents failed: %w", err)
	}
	if os.Getenv("LYNX_DEBUG") != "" {
		safe := strings.NewReplacer("$", "_", "/", "_").Replace(fileIdentifier + "_" + transactionIdentifier)
		os.WriteFile(fmt.Sprintf("/tmp/rfd_raw_%s.txt", safe), []byte(respBody), 0644)
	}
	return gwt.ParseFileDocumentsResponse(respBody)
}

func (c *LynxClient) FileDocumentSave(fileIdentifier, name, content, documentType, attachmentUrl string) error {
	body := gwt.BuildFileDocumentSaveBody(c.config.RemoteHost, fileIdentifier, name, content, documentType, attachmentUrl)
	respBody, err := c.postGWT("/lynx/service/file.rpc", body)
	if err != nil {
		return fmt.Errorf("file document save failed: %w", err)
	}
	if !strings.HasPrefix(respBody, "//OK") {
		return fmt.Errorf("file document save failed: unexpected response")
	}
	return nil
}

func (c *LynxClient) TransactionDocumentSave(fileIdentifier, transactionIdentifier, name, content, documentType, attachmentUrl string) error {
	body := gwt.BuildTransactionDocumentSaveBody(c.config.RemoteHost, fileIdentifier, transactionIdentifier, name, content, documentType, attachmentUrl)
	respBody, err := c.postGWT("/lynx/service/file.rpc", body)
	if err != nil {
		return fmt.Errorf("transaction document save failed: %w", err)
	}
	if !strings.HasPrefix(respBody, "//OK") {
		return fmt.Errorf("transaction document save failed: unexpected response")
	}
	return nil
}

func (c *LynxClient) AttachmentUpload(binary, identifier, fileName string) (string, error) {
	url, err := c.uploadAttachment(binary, identifier, fileName)
	if err != nil {
		return "", fmt.Errorf("attachment upload failed: %w", err)
	}
	return url, nil
}

func printJSON(v interface{}) {
	enc := json.NewEncoder(os.Stdout)
	enc.SetIndent("", "  ")
	enc.SetEscapeHTML(false)
	enc.Encode(v)
}
