package google

import (
	"context"
	"errors"
	"fmt"

	"github.com/PanthroCorp-Limited/openclaw-skills/google-workspace/internal/config"
	"golang.org/x/oauth2"
	"google.golang.org/api/docs/v1"
	"google.golang.org/api/option"
)

// ErrDocsReadOnly is returned when a write operation is attempted in readonly mode.
var ErrDocsReadOnly = errors.New("docs is configured as readonly; change to readwrite with 'google-workspace config set --docs=readwrite' then re-authenticate")

// DocsClient provides access to the Google Docs API with configurable
// read/write mode.
type DocsClient struct {
	svc  *docs.Service
	mode config.ServiceMode
}

// NewDocsClient creates a Docs API client using the provided token source.
func NewDocsClient(ctx context.Context, ts oauth2.TokenSource, mode config.ServiceMode) (*DocsClient, error) {
	svc, err := docs.NewService(ctx, option.WithTokenSource(ts))
	if err != nil {
		return nil, fmt.Errorf("creating docs service: %w", err)
	}
	return &DocsClient{svc: svc, mode: mode}, nil
}

// GetDocument retrieves a document by ID.
func (c *DocsClient) GetDocument(ctx context.Context, docID string) (*docs.Document, error) {
	doc, err := c.svc.Documents.Get(docID).Context(ctx).Do()
	if err != nil {
		return nil, fmt.Errorf("getting document %s: %w", docID, err)
	}
	return doc, nil
}

// InsertText inserts text at the given index. Use index 1 for the start of the
// document body. If index is 0, the text is appended to the end of the body.
// Requires readwrite mode.
func (c *DocsClient) InsertText(ctx context.Context, docID string, text string, index int64) error {
	if c.mode != config.ModeReadWrite {
		return ErrDocsReadOnly
	}

	var loc *docs.Location
	if index > 0 {
		loc = &docs.Location{Index: index}
	} else {
		loc = &docs.Location{Index: 1}
	}

	req := &docs.BatchUpdateDocumentRequest{
		Requests: []*docs.Request{
			{
				InsertText: &docs.InsertTextRequest{
					Text:     text,
					Location: loc,
				},
			},
		},
	}

	_, err := c.svc.Documents.BatchUpdate(docID, req).Context(ctx).Do()
	if err != nil {
		return fmt.Errorf("inserting text in %s: %w", docID, err)
	}
	return nil
}

// ReplaceAllText replaces all occurrences of find with replace in the document.
// Requires readwrite mode.
func (c *DocsClient) ReplaceAllText(ctx context.Context, docID, find, replace string) (*docs.BatchUpdateDocumentResponse, error) {
	if c.mode != config.ModeReadWrite {
		return nil, ErrDocsReadOnly
	}

	req := &docs.BatchUpdateDocumentRequest{
		Requests: []*docs.Request{
			{
				ReplaceAllText: &docs.ReplaceAllTextRequest{
					ContainsText: &docs.SubstringMatchCriteria{
						Text:      find,
						MatchCase: true,
					},
					ReplaceText: replace,
				},
			},
		},
	}

	resp, err := c.svc.Documents.BatchUpdate(docID, req).Context(ctx).Do()
	if err != nil {
		return nil, fmt.Errorf("replacing text in %s: %w", docID, err)
	}
	return resp, nil
}

// BatchUpdate performs a raw batch update. Requires readwrite mode.
func (c *DocsClient) BatchUpdate(ctx context.Context, docID string, requests []*docs.Request) (*docs.BatchUpdateDocumentResponse, error) {
	if c.mode != config.ModeReadWrite {
		return nil, ErrDocsReadOnly
	}

	req := &docs.BatchUpdateDocumentRequest{Requests: requests}
	resp, err := c.svc.Documents.BatchUpdate(docID, req).Context(ctx).Do()
	if err != nil {
		return nil, fmt.Errorf("batch update on %s: %w", docID, err)
	}
	return resp, nil
}
