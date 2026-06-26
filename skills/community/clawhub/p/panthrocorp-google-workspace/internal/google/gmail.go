package google

import (
	"context"
	"fmt"

	"golang.org/x/oauth2"
	"google.golang.org/api/gmail/v1"
	"google.golang.org/api/option"
)

// GmailClient provides read-only access to the Gmail API.
// No send, modify, or delete operations exist in this type.
type GmailClient struct {
	svc *gmail.Service
}

// NewGmailClient creates a Gmail API client using the provided token source.
func NewGmailClient(ctx context.Context, ts oauth2.TokenSource) (*GmailClient, error) {
	svc, err := gmail.NewService(ctx, option.WithTokenSource(ts))
	if err != nil {
		return nil, fmt.Errorf("creating gmail service: %w", err)
	}
	return &GmailClient{svc: svc}, nil
}

// SearchMessages searches for messages matching the query.
func (c *GmailClient) SearchMessages(ctx context.Context, query string, maxResults int64) ([]*gmail.Message, error) {
	call := c.svc.Users.Messages.List("me").Q(query).MaxResults(maxResults).Context(ctx)
	resp, err := call.Do()
	if err != nil {
		return nil, fmt.Errorf("searching messages: %w", err)
	}
	return resp.Messages, nil
}

// GetMessage retrieves a single message by ID.
func (c *GmailClient) GetMessage(ctx context.Context, id string, format string) (*gmail.Message, error) {
	call := c.svc.Users.Messages.Get("me", id).Format(format).Context(ctx)
	msg, err := call.Do()
	if err != nil {
		return nil, fmt.Errorf("getting message %s: %w", id, err)
	}
	return msg, nil
}

// ListLabels returns all labels for the authenticated user.
func (c *GmailClient) ListLabels(ctx context.Context) ([]*gmail.Label, error) {
	resp, err := c.svc.Users.Labels.List("me").Context(ctx).Do()
	if err != nil {
		return nil, fmt.Errorf("listing labels: %w", err)
	}
	return resp.Labels, nil
}

// GetThread retrieves a thread by ID.
func (c *GmailClient) GetThread(ctx context.Context, id string) (*gmail.Thread, error) {
	thread, err := c.svc.Users.Threads.Get("me", id).Context(ctx).Do()
	if err != nil {
		return nil, fmt.Errorf("getting thread %s: %w", id, err)
	}
	return thread, nil
}

// SearchThreads searches for threads matching the query.
func (c *GmailClient) SearchThreads(ctx context.Context, query string, maxResults int64) ([]*gmail.Thread, error) {
	resp, err := c.svc.Users.Threads.List("me").Q(query).MaxResults(maxResults).Context(ctx).Do()
	if err != nil {
		return nil, fmt.Errorf("searching threads: %w", err)
	}
	return resp.Threads, nil
}
