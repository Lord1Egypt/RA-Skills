package cmd

import (
	"context"
	"io"
	"os"

	"github.com/PanthroCorp-Limited/openclaw-skills/google-workspace/internal/config"
	gw "github.com/PanthroCorp-Limited/openclaw-skills/google-workspace/internal/google"
	"github.com/PanthroCorp-Limited/openclaw-skills/google-workspace/internal/oauth"
	"github.com/spf13/cobra"
)

var driveCmd = &cobra.Command{
	Use:   "drive",
	Short: "Read-only Google Drive operations",
}

func driveClient() (*gw.DriveClient, config.ServiceMode, context.Context) {
	ctx := context.Background()
	key := encryptionKey()
	if key == "" {
		exitf("GOOGLE_WORKSPACE_TOKEN_KEY is not set")
	}

	cfg, err := config.Load(configDir)
	if err != nil {
		exitf("loading config: %v", err)
	}
	if cfg.Drive == config.ModeOff {
		exitf("drive is disabled in config; run 'google-workspace config set --drive=readonly'")
	}

	token, err := oauth.LoadToken(configDir, key)
	if err != nil {
		exitf("%v", err)
	}

	oauthCfg := oauth.NewOAuthConfig(clientID(), clientSecret(), cfg.OAuthScopes())
	ts := oauthCfg.TokenSource(ctx, token)

	client, err := gw.NewDriveClient(ctx, ts, cfg.Drive)
	if err != nil {
		exitf("creating drive client: %v", err)
	}
	return client, cfg.Drive, ctx
}

var (
	driveListQuery      string
	driveListMaxResults int64
)

var driveListCmd = &cobra.Command{
	Use:   "list",
	Short: "List files in Google Drive",
	Run: func(cmd *cobra.Command, args []string) {
		client, _, ctx := driveClient()
		files, err := client.ListFiles(ctx, driveListQuery, driveListMaxResults)
		if err != nil {
			exitf("%v", err)
		}
		printJSON(files)
	},
}

var driveGetID string

var driveGetCmd = &cobra.Command{
	Use:   "get",
	Short: "Get file metadata by ID",
	Run: func(cmd *cobra.Command, args []string) {
		if driveGetID == "" {
			exitf("--id is required")
		}
		client, _, ctx := driveClient()
		file, err := client.GetFile(ctx, driveGetID)
		if err != nil {
			exitf("%v", err)
		}
		printJSON(file)
	},
}

var driveDownloadID string

var driveDownloadCmd = &cobra.Command{
	Use:   "download",
	Short: "Download file content to stdout",
	Long:  "Download file content to stdout. Google Docs export as plain text, Sheets as CSV, Slides as plain text. All other files download as raw bytes.",
	Run: func(cmd *cobra.Command, args []string) {
		if driveDownloadID == "" {
			exitf("--id is required")
		}
		client, _, ctx := driveClient()
		rc, err := client.DownloadFile(ctx, driveDownloadID)
		if err != nil {
			exitf("%v", err)
		}
		defer rc.Close()

		if _, err := io.Copy(os.Stdout, rc); err != nil {
			exitf("writing output: %v", err)
		}
	},
}

// Drive comments

var driveCommentsCmd = &cobra.Command{
	Use:   "comments",
	Short: "Manage comments on Drive files",
}

var (
	driveCommentsListFileID     string
	driveCommentsListMaxResults int64
)

var driveCommentsListCmd = &cobra.Command{
	Use:   "list",
	Short: "List comments on a file",
	Run: func(cmd *cobra.Command, args []string) {
		if driveCommentsListFileID == "" {
			exitf("--file-id is required")
		}
		client, _, ctx := driveClient()
		comments, err := client.ListComments(ctx, driveCommentsListFileID, driveCommentsListMaxResults)
		if err != nil {
			exitf("%v", err)
		}
		printJSON(comments)
	},
}

var (
	driveCommentFileID  string
	driveCommentContent string
)

var driveCommentCmd = &cobra.Command{
	Use:   "comment",
	Short: "Add a comment to a file (requires readwrite mode)",
	Run: func(cmd *cobra.Command, args []string) {
		if driveCommentFileID == "" {
			exitf("--file-id is required")
		}
		if driveCommentContent == "" {
			exitf("--content is required")
		}
		client, mode, ctx := driveClient()
		if mode != config.ModeReadWrite {
			exitf("drive is configured as %s; change to readwrite with 'google-workspace config set --drive=readwrite' then re-authenticate", mode)
		}
		comment, err := client.CreateComment(ctx, driveCommentFileID, driveCommentContent)
		if err != nil {
			exitf("%v", err)
		}
		printJSON(comment)
	},
}

var (
	driveReplyFileID    string
	driveReplyCommentID string
	driveReplyContent   string
)

var driveCommentReplyCmd = &cobra.Command{
	Use:   "reply",
	Short: "Reply to a comment on a file (requires readwrite mode)",
	Run: func(cmd *cobra.Command, args []string) {
		if driveReplyFileID == "" {
			exitf("--file-id is required")
		}
		if driveReplyCommentID == "" {
			exitf("--comment-id is required")
		}
		if driveReplyContent == "" {
			exitf("--content is required")
		}
		client, mode, ctx := driveClient()
		if mode != config.ModeReadWrite {
			exitf("drive is configured as %s; change to readwrite with 'google-workspace config set --drive=readwrite' then re-authenticate", mode)
		}
		reply, err := client.ReplyToComment(ctx, driveReplyFileID, driveReplyCommentID, driveReplyContent)
		if err != nil {
			exitf("%v", err)
		}
		printJSON(reply)
	},
}

func init() {
	driveListCmd.Flags().StringVar(&driveListQuery, "query", "", "Drive search query (e.g. \"name contains 'report'\")")
	driveListCmd.Flags().Int64Var(&driveListMaxResults, "max-results", 20, "maximum number of results")

	driveGetCmd.Flags().StringVar(&driveGetID, "id", "", "file ID")

	driveDownloadCmd.Flags().StringVar(&driveDownloadID, "id", "", "file ID")

	driveCommentsListCmd.Flags().StringVar(&driveCommentsListFileID, "file-id", "", "file ID")
	driveCommentsListCmd.Flags().Int64Var(&driveCommentsListMaxResults, "max-results", 20, "maximum number of comments")

	driveCommentCmd.Flags().StringVar(&driveCommentFileID, "file-id", "", "file ID")
	driveCommentCmd.Flags().StringVar(&driveCommentContent, "content", "", "comment text")

	driveCommentReplyCmd.Flags().StringVar(&driveReplyFileID, "file-id", "", "file ID")
	driveCommentReplyCmd.Flags().StringVar(&driveReplyCommentID, "comment-id", "", "comment ID to reply to")
	driveCommentReplyCmd.Flags().StringVar(&driveReplyContent, "content", "", "reply text")

	driveCommentsCmd.AddCommand(driveCommentsListCmd)
	driveCommentCmd.AddCommand(driveCommentReplyCmd)
	driveCmd.AddCommand(driveListCmd, driveGetCmd, driveDownloadCmd, driveCommentsCmd, driveCommentCmd)
	rootCmd.AddCommand(driveCmd)
}
