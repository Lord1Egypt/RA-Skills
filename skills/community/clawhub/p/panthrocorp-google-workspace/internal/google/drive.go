package google

import (
	"context"
	"errors"
	"fmt"
	"io"
	"strings"

	"github.com/PanthroCorp-Limited/openclaw-skills/google-workspace/internal/config"
	"golang.org/x/oauth2"
	"google.golang.org/api/drive/v3"
	"google.golang.org/api/option"
)

// ErrDriveReadOnly is returned when a write operation is attempted in readonly mode.
var ErrDriveReadOnly = errors.New("drive is configured as readonly; change to readwrite with 'google-workspace config set --drive=readwrite' then re-authenticate")

// googleAppsMIMEExports maps Google Workspace MIME types to their plain-text
// export equivalents. Files with these MIME types cannot be downloaded directly
// and must be exported via Files.Export instead.
var googleAppsMIMEExports = map[string]string{
	"application/vnd.google-apps.document":     "text/plain",
	"application/vnd.google-apps.spreadsheet":  "text/csv",
	"application/vnd.google-apps.presentation": "text/plain",
}

// DriveClient provides access to the Google Drive API with configurable
// read/write mode. File write operations do not exist in this type; write
// access is limited to comments.
type DriveClient struct {
	svc  *drive.Service
	mode config.ServiceMode
}

// NewDriveClient creates a Drive API client using the provided token source.
func NewDriveClient(ctx context.Context, ts oauth2.TokenSource, mode config.ServiceMode) (*DriveClient, error) {
	svc, err := drive.NewService(ctx, option.WithTokenSource(ts))
	if err != nil {
		return nil, fmt.Errorf("creating drive service: %w", err)
	}
	return &DriveClient{svc: svc, mode: mode}, nil
}

// driveFileFields is the default field mask for file list responses.
const driveFileFields = "files(id,name,mimeType,size,createdTime,modifiedTime,parents,webViewLink)"

// ListFiles returns files visible to the authenticated user.
func (c *DriveClient) ListFiles(ctx context.Context, query string, pageSize int64) ([]*drive.File, error) {
	call := c.svc.Files.List().
		PageSize(pageSize).
		Fields(driveFileFields).
		OrderBy("modifiedTime desc").
		Context(ctx)

	if query != "" {
		call = call.Q(query)
	}

	resp, err := call.Do()
	if err != nil {
		return nil, fmt.Errorf("listing files: %w", err)
	}
	return resp.Files, nil
}

// GetFile retrieves metadata for a single file.
func (c *DriveClient) GetFile(ctx context.Context, fileID string) (*drive.File, error) {
	file, err := c.svc.Files.Get(fileID).
		Fields("*").
		Context(ctx).
		Do()
	if err != nil {
		return nil, fmt.Errorf("getting file %s: %w", fileID, err)
	}
	return file, nil
}

// DownloadFile retrieves the content of a file. For Google Workspace files
// (Docs, Sheets, Slides) it exports to a text format automatically. For all
// other files it downloads the raw bytes. The caller must close the returned
// ReadCloser.
func (c *DriveClient) DownloadFile(ctx context.Context, fileID string) (io.ReadCloser, error) {
	meta, err := c.svc.Files.Get(fileID).
		Fields("id,mimeType").
		Context(ctx).
		Do()
	if err != nil {
		return nil, fmt.Errorf("getting file metadata %s: %w", fileID, err)
	}

	if exportMIME, ok := googleAppsMIMEExports[meta.MimeType]; ok {
		resp, err := c.svc.Files.Export(fileID, exportMIME).Context(ctx).Download()
		if err != nil {
			return nil, fmt.Errorf("exporting file %s as %s: %w", fileID, exportMIME, err)
		}
		return resp.Body, nil
	}

	resp, err := c.svc.Files.Get(fileID).Context(ctx).Download()
	if err != nil {
		return nil, fmt.Errorf("downloading file %s: %w", fileID, err)
	}
	return resp.Body, nil
}

// IsGoogleAppsFile reports whether the MIME type is a Google Workspace type
// that requires export rather than direct download.
func IsGoogleAppsFile(mimeType string) bool {
	return strings.HasPrefix(mimeType, "application/vnd.google-apps.")
}

// ListComments returns comments on a file. Works in both readonly and readwrite modes.
func (c *DriveClient) ListComments(ctx context.Context, fileID string, maxResults int64) ([]*drive.Comment, error) {
	resp, err := c.svc.Comments.List(fileID).
		PageSize(maxResults).
		Fields("comments(id,author(displayName,emailAddress),content,createdTime,resolved,replies(id,author(displayName,emailAddress),content,createdTime))").
		Context(ctx).
		Do()
	if err != nil {
		return nil, fmt.Errorf("listing comments on %s: %w", fileID, err)
	}
	return resp.Comments, nil
}

// CreateComment adds a comment to a file. Requires readwrite mode.
func (c *DriveClient) CreateComment(ctx context.Context, fileID, content string) (*drive.Comment, error) {
	if c.mode != config.ModeReadWrite {
		return nil, ErrDriveReadOnly
	}
	comment, err := c.svc.Comments.Create(fileID, &drive.Comment{Content: content}).
		Fields("id,author(displayName,emailAddress),content,createdTime").
		Context(ctx).
		Do()
	if err != nil {
		return nil, fmt.Errorf("creating comment on %s: %w", fileID, err)
	}
	return comment, nil
}

// ReplyToComment replies to an existing comment. Requires readwrite mode.
func (c *DriveClient) ReplyToComment(ctx context.Context, fileID, commentID, content string) (*drive.Reply, error) {
	if c.mode != config.ModeReadWrite {
		return nil, ErrDriveReadOnly
	}
	reply, err := c.svc.Replies.Create(fileID, commentID, &drive.Reply{Content: content}).
		Fields("id,author(displayName,emailAddress),content,createdTime").
		Context(ctx).
		Do()
	if err != nil {
		return nil, fmt.Errorf("replying to comment %s on %s: %w", commentID, fileID, err)
	}
	return reply, nil
}
