// Package imap provides IMAP client functionality for nmail.
package imap

import (
	"context"
	"crypto/tls"
	"errors"
	"fmt"
	"io"
	"mime"
	"sort"
	"strings"
	"time"

	"github.com/emersion/go-imap/v2"
	"github.com/emersion/go-imap/v2/imapclient"
	"github.com/emersion/go-message/charset"
	"github.com/harlock/nmail/internal/config"
	"golang.org/x/text/encoding/korean"
	"golang.org/x/text/transform"
)

func init() {
	// Register Korean charset decoders for go-message
	charset.RegisterEncoding("euc-kr", korean.EUCKR)
	charset.RegisterEncoding("ks_c_5601-1987", korean.EUCKR)
}

// Message represents a parsed email message.
type Message struct {
	ID      uint32    `json:"id"`
	From    string    `json:"from"`
	Subject string    `json:"subject"`
	Date    time.Time `json:"date"`
	Body    string    `json:"body,omitempty"`
	IsRead  bool      `json:"is_read"`
}

// SearchQuery represents filters for searching messages.
type SearchQuery struct {
	From    string
	Subject string
	Text    string
	Since   time.Time
	Before  time.Time
	Unseen  bool
	Limit   int
}

// Client wraps an IMAP connection.
type Client struct {
	c *imapclient.Client
}

// ErrIdleUnsupported indicates the IMAP server rejected the IDLE command.
var ErrIdleUnsupported = errors.New("imap idle unsupported")

type mailboxStatus struct {
	uidNext     imap.UID
	uidValidity uint32
}

// Connect opens a TLS IMAP connection and logs in.
func Connect(account config.Account) (*Client, error) {
	addr := fmt.Sprintf("%s:%d", account.IMAPHost, account.IMAPPort)

	var c *imapclient.Client
	var err error

	options := &imapclient.Options{
		TLSConfig: &tls.Config{ServerName: account.IMAPHost},
	}
	if account.IMAPTLS {
		c, err = imapclient.DialTLS(addr, options)
	} else {
		c, err = imapclient.DialInsecure(addr, nil)
	}
	if err != nil {
		return nil, fmt.Errorf("connecting to %s: %w", addr, err)
	}

	if err := c.Login(account.Email, account.Password).Wait(); err != nil {
		c.Close()
		return nil, fmt.Errorf("login failed: %w", err)
	}
	return &Client{c: c}, nil
}

// Close closes the IMAP connection.
func (cl *Client) Close() error {
	return cl.c.Logout().Wait()
}

// FetchInbox returns the latest `limit` messages from INBOX (headers only).
func (cl *Client) FetchInbox(limit int) ([]Message, error) {
	if _, err := cl.selectInbox(); err != nil {
		return nil, err
	}

	searchData, err := cl.c.Search(&imap.SearchCriteria{}, nil).Wait()
	if err != nil {
		return nil, fmt.Errorf("searching messages: %w", err)
	}

	ids := searchData.AllSeqNums()
	if len(ids) == 0 {
		return []Message{}, nil
	}

	if limit > 0 && len(ids) > limit {
		ids = ids[len(ids)-limit:]
	}
	reverseSeqNums(ids)

	return cl.fetchMessagesBySeqNums(ids, false)
}

// SearchMessages returns messages in INBOX matching the provided filters.
func (cl *Client) SearchMessages(query SearchQuery) ([]Message, error) {
	if _, err := cl.selectInbox(); err != nil {
		return nil, err
	}

	criteria := &imap.SearchCriteria{}
	if query.From != "" {
		criteria.Header = append(criteria.Header, imap.SearchCriteriaHeaderField{Key: "FROM", Value: query.From})
	}
	if query.Subject != "" {
		criteria.Header = append(criteria.Header, imap.SearchCriteriaHeaderField{Key: "SUBJECT", Value: query.Subject})
	}
	if query.Text != "" {
		criteria.Text = append(criteria.Text, query.Text)
	}
	if !query.Since.IsZero() {
		criteria.Since = query.Since
	}
	if !query.Before.IsZero() {
		criteria.Before = query.Before
	}
	if query.Unseen {
		criteria.NotFlag = append(criteria.NotFlag, imap.FlagSeen)
	}

	searchData, err := cl.c.Search(criteria, nil).Wait()
	if err != nil {
		return nil, fmt.Errorf("searching messages: %w", err)
	}

	ids := searchData.AllSeqNums()
	if len(ids) == 0 {
		return []Message{}, nil
	}

	if query.Limit > 0 && len(ids) > query.Limit {
		ids = ids[len(ids)-query.Limit:]
	}
	reverseSeqNums(ids)

	return cl.fetchMessagesBySeqNums(ids, false)
}

// FetchMessage returns the full message including body.
func (cl *Client) FetchMessage(id uint32) (*Message, error) {
	if _, err := cl.selectInbox(); err != nil {
		return nil, err
	}

	msgs, err := cl.fetchMessagesBySeqNums([]uint32{id}, true)
	if err != nil {
		return nil, err
	}
	if len(msgs) == 0 {
		return nil, fmt.Errorf("message %d not found", id)
	}

	msg := msgs[0]
	return &msg, nil
}

// Watch watches INBOX for new messages, preferring IMAP IDLE and falling back to polling when IDLE isn't supported.
func (cl *Client) Watch(ctx context.Context, fallbackPollInterval time.Duration, onNew func(Message) error) error {
	err := cl.WatchIDLE(ctx, onNew)
	if err == nil || ctx.Err() != nil || !errors.Is(err, ErrIdleUnsupported) {
		return err
	}
	return cl.WatchPoll(ctx, fallbackPollInterval, onNew)
}

// WatchIDLE watches INBOX for new messages using IMAP IDLE.
func (cl *Client) WatchIDLE(ctx context.Context, onNew func(Message) error) error {
	if onNew == nil {
		return fmt.Errorf("watch callback is required")
	}

	selected, err := cl.selectInbox()
	if err != nil {
		return err
	}
	if !cl.supportsIdle() {
		return ErrIdleUnsupported
	}

	lastCount := selected.NumMessages
	checkTicker := time.NewTicker(time.Second)
	defer checkTicker.Stop()

	for {
		if err := ctx.Err(); err != nil {
			return nil
		}

		idleCmd, err := cl.c.Idle()
		if err != nil {
			if isIdleUnsupportedError(err) {
				return fmt.Errorf("%w: %v", ErrIdleUnsupported, err)
			}
			return fmt.Errorf("starting IDLE: %w", err)
		}

		waitCh := make(chan error, 1)
		go func() {
			waitCh <- idleCmd.Wait()
		}()

		shouldRestart := false
		for !shouldRestart {
			select {
			case <-ctx.Done():
				return stopIdle(idleCmd, waitCh)
			case err := <-waitCh:
				if err != nil {
					if isIdleUnsupportedError(err) {
						return fmt.Errorf("%w: %v", ErrIdleUnsupported, err)
					}
					return fmt.Errorf("waiting for IDLE: %w", err)
				}
				shouldRestart = true
			case <-checkTicker.C:
				currentCount := cl.mailboxCount()
				switch {
				case currentCount > lastCount:
					if err := stopIdle(idleCmd, waitCh); err != nil {
						return err
					}
					if err := cl.emitNewMessages(lastCount, currentCount, onNew); err != nil {
						return err
					}
					lastCount = currentCount
					shouldRestart = true
				case currentCount < lastCount:
					lastCount = currentCount
				}
			}
		}
	}
}

// WatchPoll watches INBOX for new messages by polling mailbox UIDNEXT.
func (cl *Client) WatchPoll(ctx context.Context, interval time.Duration, onNew func(Message) error) error {
	if onNew == nil {
		return fmt.Errorf("watch callback is required")
	}
	if interval <= 0 {
		return fmt.Errorf("poll interval must be greater than zero")
	}

	// Get initial UIDNEXT via SELECT (not STATUS — Naver caches STATUS results)
	selected, err := cl.selectInbox()
	if err != nil {
		return err
	}
	lastUIDNext := selected.UIDNext

	ticker := time.NewTicker(interval)
	defer ticker.Stop()

	for {
		select {
		case <-ctx.Done():
			return nil
		case <-ticker.C:
			// Re-SELECT to get fresh UIDNEXT (Naver doesn't update STATUS for selected mailbox)
			reselected, err := cl.c.Select("INBOX", nil).Wait()
			if err != nil {
				return fmt.Errorf("re-selecting INBOX: %w", err)
			}
			currentUIDNext := reselected.UIDNext

			if currentUIDNext > lastUIDNext {
				if err := cl.emitNewMessagesByUID(lastUIDNext, currentUIDNext, onNew); err != nil {
					return err
				}
				lastUIDNext = currentUIDNext
			} else if currentUIDNext < lastUIDNext {
				// UIDVALIDITY changed, reset
				lastUIDNext = currentUIDNext
			}
		}
	}
}

func (cl *Client) selectInbox() (*imap.SelectData, error) {
	selected, err := cl.c.Select("INBOX", nil).Wait()
	if err != nil {
		return nil, fmt.Errorf("selecting INBOX: %w", err)
	}
	return selected, nil
}

func (cl *Client) inboxStatus() (mailboxStatus, error) {
	data, err := cl.c.Status("INBOX", &imap.StatusOptions{UIDNext: true, UIDValidity: true}).Wait()
	if err != nil {
		return mailboxStatus{}, fmt.Errorf("checking INBOX status: %w", err)
	}
	return mailboxStatus{uidNext: data.UIDNext, uidValidity: data.UIDValidity}, nil
}

func (cl *Client) supportsIdle() bool {
	caps := cl.c.Caps()
	return caps.Has(imap.CapIMAP4rev2) || caps.Has(imap.CapIdle)
}

func (cl *Client) fetchMessagesBySeqNums(seqNums []uint32, includeBody bool) ([]Message, error) {
	if len(seqNums) == 0 {
		return []Message{}, nil
	}

	fetchOptions := &imap.FetchOptions{
		Envelope: true,
		Flags:    true,
		UID:      true,
	}
	if includeBody {
		fetchOptions.BodySection = []*imap.FetchItemBodySection{{}}
	}

	msgBuffers, err := cl.c.Fetch(imap.SeqSetNum(seqNums...), fetchOptions).Collect()
	if err != nil {
		if includeBody {
			return nil, fmt.Errorf("fetching message: %w", err)
		}
		return nil, fmt.Errorf("fetching messages: %w", err)
	}
	if len(msgBuffers) == 0 {
		return []Message{}, nil
	}

	bySeqNum := make(map[uint32]Message, len(msgBuffers))
	for _, msg := range msgBuffers {
		parsed := parseMessageBuffer(msg)
		if includeBody {
			for _, section := range msg.BodySection {
				if len(section.Bytes) > 0 {
					parsed.Body = extractPlainText(section.Bytes)
					break
				}
			}
		}
		bySeqNum[msg.SeqNum] = parsed
	}

	result := make([]Message, 0, len(seqNums))
	for _, seqNum := range seqNums {
		if msg, ok := bySeqNum[seqNum]; ok {
			result = append(result, msg)
		}
	}
	return result, nil
}

func (cl *Client) fetchMessagesByUIDSet(uidSet imap.UIDSet, includeBody bool) ([]Message, error) {
	if len(uidSet) == 0 {
		return []Message{}, nil
	}

	fetchOptions := &imap.FetchOptions{
		Envelope: true,
		Flags:    true,
		UID:      true,
	}
	if includeBody {
		fetchOptions.BodySection = []*imap.FetchItemBodySection{{}}
	}

	msgBuffers, err := cl.c.Fetch(uidSet, fetchOptions).Collect()
	if err != nil {
		if includeBody {
			return nil, fmt.Errorf("fetching message by UID: %w", err)
		}
		return nil, fmt.Errorf("fetching messages by UID: %w", err)
	}
	if len(msgBuffers) == 0 {
		return []Message{}, nil
	}

	sort.Slice(msgBuffers, func(i, j int) bool {
		return msgBuffers[i].UID < msgBuffers[j].UID
	})

	result := make([]Message, 0, len(msgBuffers))
	for _, msg := range msgBuffers {
		parsed := parseMessageBuffer(msg)
		if includeBody {
			for _, section := range msg.BodySection {
				if len(section.Bytes) > 0 {
					parsed.Body = extractPlainText(section.Bytes)
					break
				}
			}
		}
		result = append(result, parsed)
	}
	return result, nil
}

func (cl *Client) emitNewMessages(lastCount, currentCount uint32, onNew func(Message) error) error {
	if currentCount <= lastCount {
		return nil
	}

	seqNums := make([]uint32, 0, currentCount-lastCount)
	for seqNum := lastCount + 1; seqNum <= currentCount; seqNum++ {
		seqNums = append(seqNums, seqNum)
	}

	msgs, err := cl.fetchMessagesBySeqNums(seqNums, false)
	if err != nil {
		return err
	}
	for _, msg := range msgs {
		if err := onNew(msg); err != nil {
			return err
		}
	}
	return nil
}

func (cl *Client) emitNewMessagesByUID(lastUIDNext, currentUIDNext imap.UID, onNew func(Message) error) error {
	if currentUIDNext <= lastUIDNext || lastUIDNext == 0 {
		return nil
	}

	var uidSet imap.UIDSet
	uidSet.AddRange(lastUIDNext, currentUIDNext-1)

	msgs, err := cl.fetchMessagesByUIDSet(uidSet, false)
	if err != nil {
		return err
	}
	for _, msg := range msgs {
		if err := onNew(msg); err != nil {
			return err
		}
	}
	return nil
}

func (cl *Client) mailboxCount() uint32 {
	mailbox := cl.c.Mailbox()
	if mailbox == nil {
		return 0
	}
	return mailbox.NumMessages
}

func isIdleUnsupportedError(err error) bool {
	if err == nil {
		return false
	}

	msg := strings.ToLower(err.Error())
	return strings.Contains(msg, "idle") &&
		(strings.Contains(msg, " bad") ||
			strings.Contains(msg, "unsupported") ||
			strings.Contains(msg, "not supported") ||
			strings.Contains(msg, "unknown command") ||
			strings.Contains(msg, "capability"))
}

func stopIdle(idleCmd *imapclient.IdleCommand, waitCh <-chan error) error {
	if err := idleCmd.Close(); err != nil && !strings.Contains(err.Error(), "already closed") {
		return fmt.Errorf("stopping IDLE: %w", err)
	}
	if err := <-waitCh; err != nil {
		return fmt.Errorf("waiting for IDLE: %w", err)
	}
	return nil
}

func parseMessageBuffer(msg *imapclient.FetchMessageBuffer) Message {
	m := Message{
		ID:     msg.SeqNum,
		IsRead: containsFlag(msg.Flags, imap.FlagSeen),
	}
	if msg.Envelope != nil {
		m.Subject = decodeHeader(msg.Envelope.Subject)
		m.Date = msg.Envelope.Date
		if len(msg.Envelope.From) > 0 {
			m.From = formatAddress(msg.Envelope.From[0])
		}
	}
	return m
}

func formatAddress(addr imap.Address) string {
	if addr.Name != "" {
		return fmt.Sprintf("%s <%s@%s>", decodeHeader(addr.Name), addr.Mailbox, addr.Host)
	}
	return fmt.Sprintf("%s@%s", addr.Mailbox, addr.Host)
}

func reverseSeqNums(nums []uint32) {
	for i, j := 0, len(nums)-1; i < j; i, j = i+1, j-1 {
		nums[i], nums[j] = nums[j], nums[i]
	}
}

// decodeHeader decodes RFC 2047 encoded headers (handles EUC-KR).
func decodeHeader(s string) string {
	dec := new(mime.WordDecoder)
	dec.CharsetReader = func(cs string, r io.Reader) (io.Reader, error) {
		cs = strings.ToLower(strings.ReplaceAll(cs, "-", ""))
		switch cs {
		case "euckr", "ksc56011987":
			return transform.NewReader(r, korean.EUCKR.NewDecoder()), nil
		}
		return r, nil
	}
	decoded, err := dec.DecodeHeader(s)
	if err != nil {
		return s
	}
	return decoded
}

// extractPlainText attempts to get plain text from a raw message body.
func extractPlainText(body []byte) string {
	s := string(body)
	// Very basic: strip headers, return body
	if idx := strings.Index(s, "\r\n\r\n"); idx >= 0 {
		return strings.TrimSpace(s[idx+4:])
	}
	if idx := strings.Index(s, "\n\n"); idx >= 0 {
		return strings.TrimSpace(s[idx+2:])
	}
	return strings.TrimSpace(s)
}

func containsFlag(flags []imap.Flag, target imap.Flag) bool {
	for _, flag := range flags {
		if flag == target {
			return true
		}
	}
	return false
}
