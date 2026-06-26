package cmd

import (
	"context"
	"fmt"
	"strings"

	"github.com/PanthroCorp-Limited/openclaw-skills/zoho-mail/internal/oauth"
	"github.com/PanthroCorp-Limited/openclaw-skills/zoho-mail/internal/zoho"
	"github.com/spf13/cobra"
	"golang.org/x/oauth2"
)

var mailCmd = &cobra.Command{
	Use:   "mail",
	Short: "Read, send, and manage email",
}

func zohoClient() (*zoho.Client, context.Context) {
	ctx := context.Background()

	key := encryptionKey()
	if key == "" {
		exitf("ZOHO_MAIL_TOKEN_KEY is not set")
	}

	cID := clientID()
	cSecret := clientSecret()
	if cID == "" || cSecret == "" {
		exitf("ZOHO_CLIENT_ID and ZOHO_CLIENT_SECRET must be set")
	}

	cfg, err := loadConfig(configDir)
	if err != nil {
		exitf("loading config: %v", err)
	}
	if cfg.Email == "" {
		exitf("email not configured; run 'zoho-mail config set --email your@address.com'")
	}

	token, err := oauth.LoadToken(configDir, key)
	if err != nil {
		exitf("%v", err)
	}

	oauthCfg := oauth.NewOAuthConfig(cID, cSecret)
	ts := oauthCfg.TokenSource(ctx, token)

	// Wrap the token source so that a refreshed token is persisted back to disk.
	pts := &persistingTokenSource{inner: ts, dir: configDir, key: key}

	client := zoho.NewClient(ctx, pts, cfg.Email)
	return client, ctx
}

// persistingTokenSource wraps an oauth2.TokenSource and saves refreshed tokens to disk.
type persistingTokenSource struct {
	inner oauth2.TokenSource
	dir   string
	key   string
	last  *oauth2.Token
}

func (p *persistingTokenSource) Token() (*oauth2.Token, error) {
	t, err := p.inner.Token()
	if err != nil {
		return nil, err
	}
	// Save if the token changed (i.e. was refreshed).
	if p.last == nil || t.AccessToken != p.last.AccessToken {
		_ = oauth.SaveToken(p.dir, t, p.key) // best-effort; don't fail the request
		p.last = t
	}
	return t, nil
}

// mail list

var (
	listFolder string
	listLimit  int
	listStart  int
)

var mailListCmd = &cobra.Command{
	Use:   "list",
	Short: "List messages in a folder",
	Run: func(cmd *cobra.Command, args []string) {
		client, ctx := zohoClient()
		messages, err := client.ListMessages(ctx, listFolder, listLimit, listStart)
		if err != nil {
			exitf("%v", err)
		}
		printJSON(messages)
	},
}

// mail read

var readID string

var mailReadCmd = &cobra.Command{
	Use:   "read",
	Short: "Read a message by ID",
	Run: func(cmd *cobra.Command, args []string) {
		if readID == "" {
			exitf("--id is required")
		}
		client, ctx := zohoClient()
		msg, err := client.GetMessage(ctx, readID)
		if err != nil {
			exitf("%v", err)
		}
		printJSON(msg)
	},
}

// mail send

var (
	sendTo      string
	sendCC      string
	sendSubject string
	sendBody    string
	sendHTML    bool
)

var mailSendCmd = &cobra.Command{
	Use:   "send",
	Short: "Send a new email",
	Run: func(cmd *cobra.Command, args []string) {
		if sendTo == "" {
			exitf("--to is required")
		}
		if sendSubject == "" {
			exitf("--subject is required")
		}
		if sendBody == "" {
			exitf("--body is required")
		}

		cfg, err := loadConfig(configDir)
		if err != nil {
			exitf("loading config: %v", err)
		}

		format := "plaintext"
		if sendHTML {
			format = "html"
		}

		req := zoho.SendRequest{
			FromAddress: cfg.Email,
			ToAddress:   sendTo,
			CCAddress:   sendCC,
			Subject:     sendSubject,
			Content:     sendBody,
			MailFormat:  format,
		}

		client, ctx := zohoClient()
		sent, err := client.SendMessage(ctx, req)
		if err != nil {
			exitf("%v", err)
		}
		printJSON(sent)
	},
}

// mail reply

var (
	replyID   string
	replyBody string
	replyHTML bool
)

var mailReplyCmd = &cobra.Command{
	Use:   "reply",
	Short: "Reply to a message",
	Run: func(cmd *cobra.Command, args []string) {
		if replyID == "" {
			exitf("--id is required")
		}
		if replyBody == "" {
			exitf("--body is required")
		}

		client, ctx := zohoClient()

		original, err := client.GetMessage(ctx, replyID)
		if err != nil {
			exitf("fetching original message: %v", err)
		}

		cfg, err := loadConfig(configDir)
		if err != nil {
			exitf("loading config: %v", err)
		}

		subject := original.Subject
		if !strings.HasPrefix(strings.ToLower(subject), "re:") {
			subject = "Re: " + subject
		}

		format := "plaintext"
		if replyHTML {
			format = "html"
		}

		req := zoho.SendRequest{
			FromAddress: cfg.Email,
			ToAddress:   original.FromAddress,
			Subject:     subject,
			Content:     replyBody,
			MailFormat:  format,
			InReplyTo:   original.MessageID,
		}

		sent, err := client.SendMessage(ctx, req)
		if err != nil {
			exitf("%v", err)
		}
		printJSON(sent)
	},
}

// mail search

var (
	searchQuery string
	searchLimit int
)

var mailSearchCmd = &cobra.Command{
	Use:   "search",
	Short: "Search messages",
	Run: func(cmd *cobra.Command, args []string) {
		if searchQuery == "" {
			exitf("--query is required")
		}
		client, ctx := zohoClient()
		messages, err := client.SearchMessages(ctx, searchQuery, searchLimit)
		if err != nil {
			exitf("%v", err)
		}
		printJSON(messages)
	},
}

// mail delete

var (
	deleteID       string
	deleteFolderID string
)

var mailDeleteCmd = &cobra.Command{
	Use:   "delete",
	Short: "Delete a message",
	Run: func(cmd *cobra.Command, args []string) {
		if deleteID == "" {
			exitf("--id is required")
		}
		client, ctx := zohoClient()
		if err := client.DeleteMessage(ctx, deleteID, deleteFolderID); err != nil {
			exitf("%v", err)
		}
		fmt.Printf("Message %s deleted.\n", deleteID)
	},
}

// mail mark

var (
	markIDs    string
	markRead   bool
	markUnread bool
)

var mailMarkCmd = &cobra.Command{
	Use:   "mark",
	Short: "Mark messages as read or unread",
	Run: func(cmd *cobra.Command, args []string) {
		if markIDs == "" {
			exitf("--ids is required")
		}
		if !markRead && !markUnread {
			exitf("one of --read or --unread is required")
		}
		if markRead && markUnread {
			exitf("--read and --unread are mutually exclusive")
		}

		ids := strings.Split(markIDs, ",")
		for i, id := range ids {
			ids[i] = strings.TrimSpace(id)
		}

		client, ctx := zohoClient()
		if err := client.MarkRead(ctx, ids, markRead); err != nil {
			exitf("%v", err)
		}
		fmt.Printf("Marked %d message(s).\n", len(ids))
	},
}

func init() {
	mailListCmd.Flags().StringVar(&listFolder, "folder", "", "folder ID (default: INBOX)")
	mailListCmd.Flags().IntVar(&listLimit, "limit", 20, "maximum number of messages to return")
	mailListCmd.Flags().IntVar(&listStart, "start", 0, "offset for pagination")

	mailReadCmd.Flags().StringVar(&readID, "id", "", "message ID")

	mailSendCmd.Flags().StringVar(&sendTo, "to", "", "recipient email address")
	mailSendCmd.Flags().StringVar(&sendCC, "cc", "", "CC email address")
	mailSendCmd.Flags().StringVar(&sendSubject, "subject", "", "email subject")
	mailSendCmd.Flags().StringVar(&sendBody, "body", "", "email body")
	mailSendCmd.Flags().BoolVar(&sendHTML, "html", false, "send body as HTML")

	mailReplyCmd.Flags().StringVar(&replyID, "id", "", "message ID to reply to")
	mailReplyCmd.Flags().StringVar(&replyBody, "body", "", "reply body")
	mailReplyCmd.Flags().BoolVar(&replyHTML, "html", false, "send reply as HTML")

	mailSearchCmd.Flags().StringVar(&searchQuery, "query", "", "search query")
	mailSearchCmd.Flags().IntVar(&searchLimit, "limit", 20, "maximum number of results")

	mailDeleteCmd.Flags().StringVar(&deleteID, "id", "", "message ID")
	mailDeleteCmd.Flags().StringVar(&deleteFolderID, "folder", "", "folder ID containing the message")

	mailMarkCmd.Flags().StringVar(&markIDs, "ids", "", "comma-separated list of message IDs")
	mailMarkCmd.Flags().BoolVar(&markRead, "read", false, "mark as read")
	mailMarkCmd.Flags().BoolVar(&markUnread, "unread", false, "mark as unread")

	mailCmd.AddCommand(mailListCmd, mailReadCmd, mailSendCmd, mailReplyCmd, mailSearchCmd, mailDeleteCmd, mailMarkCmd)
	rootCmd.AddCommand(mailCmd)
}
