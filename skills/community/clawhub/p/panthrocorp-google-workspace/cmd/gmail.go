package cmd

import (
	"context"
	"encoding/json"
	"fmt"

	"github.com/PanthroCorp-Limited/openclaw-skills/google-workspace/internal/config"
	gw "github.com/PanthroCorp-Limited/openclaw-skills/google-workspace/internal/google"
	"github.com/PanthroCorp-Limited/openclaw-skills/google-workspace/internal/oauth"
	"github.com/spf13/cobra"
	"golang.org/x/oauth2"
)

var gmailCmd = &cobra.Command{
	Use:   "gmail",
	Short: "Read-only Gmail operations",
}

func gmailClient() (*gw.GmailClient, context.Context) {
	ctx := context.Background()
	key := encryptionKey()
	if key == "" {
		exitf("GOOGLE_WORKSPACE_TOKEN_KEY is not set")
	}

	cfg, err := config.Load(configDir)
	if err != nil {
		exitf("loading config: %v", err)
	}
	if !cfg.Gmail {
		exitf("gmail is disabled in config; run 'google-workspace config set --gmail=true'")
	}

	token, err := oauth.LoadToken(configDir, key)
	if err != nil {
		exitf("%v", err)
	}

	oauthCfg := oauth.NewOAuthConfig(clientID(), clientSecret(), cfg.OAuthScopes())
	ts := oauthCfg.TokenSource(ctx, token)

	client, err := gw.NewGmailClient(ctx, ts)
	if err != nil {
		exitf("creating gmail client: %v", err)
	}
	return client, ctx
}

func printJSON(v any) {
	data, _ := json.MarshalIndent(v, "", "  ")
	fmt.Println(string(data))
}

var (
	gmailSearchQuery      string
	gmailSearchMaxResults int64
)

var gmailSearchCmd = &cobra.Command{
	Use:   "search",
	Short: "Search Gmail messages",
	Run: func(cmd *cobra.Command, args []string) {
		client, ctx := gmailClient()
		messages, err := client.SearchMessages(ctx, gmailSearchQuery, gmailSearchMaxResults)
		if err != nil {
			exitf("%v", err)
		}

		if outputFmt == "json" {
			printJSON(messages)
			return
		}

		for _, msg := range messages {
			fmt.Printf("ID: %s  ThreadID: %s\n", msg.Id, msg.ThreadId)
		}
	},
}

var (
	gmailReadID     string
	gmailReadFormat string
)

var gmailReadCmd = &cobra.Command{
	Use:   "read",
	Short: "Read a specific message by ID",
	Run: func(cmd *cobra.Command, args []string) {
		if gmailReadID == "" {
			exitf("--id is required")
		}
		client, ctx := gmailClient()
		msg, err := client.GetMessage(ctx, gmailReadID, gmailReadFormat)
		if err != nil {
			exitf("%v", err)
		}
		printJSON(msg)
	},
}

var gmailLabelsCmd = &cobra.Command{
	Use:   "labels",
	Short: "List all Gmail labels",
	Run: func(cmd *cobra.Command, args []string) {
		client, ctx := gmailClient()
		labels, err := client.ListLabels(ctx)
		if err != nil {
			exitf("%v", err)
		}
		printJSON(labels)
	},
}

var (
	gmailThreadsQuery      string
	gmailThreadsID         string
	gmailThreadsMaxResults int64
)

var gmailThreadsCmd = &cobra.Command{
	Use:   "threads",
	Short: "List or read Gmail threads",
	Run: func(cmd *cobra.Command, args []string) {
		client, ctx := gmailClient()

		if gmailThreadsID != "" {
			thread, err := client.GetThread(ctx, gmailThreadsID)
			if err != nil {
				exitf("%v", err)
			}
			printJSON(thread)
			return
		}

		threads, err := client.SearchThreads(ctx, gmailThreadsQuery, gmailThreadsMaxResults)
		if err != nil {
			exitf("%v", err)
		}
		printJSON(threads)
	},
}

// tokenSourceFromConfig is a helper that creates an auto-refreshing token source.
var _ oauth2.TokenSource // ensure import is used

func init() {
	gmailSearchCmd.Flags().StringVar(&gmailSearchQuery, "query", "", "Gmail search query")
	gmailSearchCmd.Flags().Int64Var(&gmailSearchMaxResults, "max-results", 10, "maximum number of results")

	gmailReadCmd.Flags().StringVar(&gmailReadID, "id", "", "message ID to read")
	gmailReadCmd.Flags().StringVar(&gmailReadFormat, "format", "full", "message format: full, metadata, minimal, or raw")

	gmailThreadsCmd.Flags().StringVar(&gmailThreadsQuery, "query", "", "search query for threads")
	gmailThreadsCmd.Flags().StringVar(&gmailThreadsID, "id", "", "thread ID to read (if set, query is ignored)")
	gmailThreadsCmd.Flags().Int64Var(&gmailThreadsMaxResults, "max-results", 10, "maximum number of results")

	gmailCmd.AddCommand(gmailSearchCmd, gmailReadCmd, gmailLabelsCmd, gmailThreadsCmd)
	rootCmd.AddCommand(gmailCmd)
}
