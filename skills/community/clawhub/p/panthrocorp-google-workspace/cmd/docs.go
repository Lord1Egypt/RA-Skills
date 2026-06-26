package cmd

import (
	"context"

	"github.com/PanthroCorp-Limited/openclaw-skills/google-workspace/internal/config"
	gw "github.com/PanthroCorp-Limited/openclaw-skills/google-workspace/internal/google"
	"github.com/PanthroCorp-Limited/openclaw-skills/google-workspace/internal/oauth"
	"github.com/spf13/cobra"
)

var docsCmd = &cobra.Command{
	Use:   "docs",
	Short: "Google Docs operations",
}

func docsClient() (*gw.DocsClient, config.ServiceMode, context.Context) {
	ctx := context.Background()
	key := encryptionKey()
	if key == "" {
		exitf("GOOGLE_WORKSPACE_TOKEN_KEY is not set")
	}

	cfg, err := config.Load(configDir)
	if err != nil {
		exitf("loading config: %v", err)
	}
	if cfg.Docs == config.ModeOff {
		exitf("docs is disabled in config; run 'google-workspace config set --docs=readonly'")
	}

	token, err := oauth.LoadToken(configDir, key)
	if err != nil {
		exitf("%v", err)
	}

	oauthCfg := oauth.NewOAuthConfig(clientID(), clientSecret(), cfg.OAuthScopes())
	ts := oauthCfg.TokenSource(ctx, token)

	client, err := gw.NewDocsClient(ctx, ts, cfg.Docs)
	if err != nil {
		exitf("creating docs client: %v", err)
	}
	return client, cfg.Docs, ctx
}

var docsReadDocID string

var docsReadCmd = &cobra.Command{
	Use:   "read",
	Short: "Read a document",
	Run: func(cmd *cobra.Command, args []string) {
		if docsReadDocID == "" {
			exitf("--document-id is required")
		}
		client, _, ctx := docsClient()
		doc, err := client.GetDocument(ctx, docsReadDocID)
		if err != nil {
			exitf("%v", err)
		}
		printJSON(doc)
	},
}

var (
	docsEditDocID       string
	docsEditInsertText  string
	docsEditIndex       int64
	docsEditFind        string
	docsEditReplaceWith string
)

var docsEditCmd = &cobra.Command{
	Use:   "edit",
	Short: "Edit a document (requires readwrite mode)",
	Long: `Edit a document using one of two modes:

  Insert text:       --insert-text TEXT [--index N]
  Find and replace:  --find TEXT --replace-with TEXT`,
	Run: func(cmd *cobra.Command, args []string) {
		if docsEditDocID == "" {
			exitf("--document-id is required")
		}

		client, mode, ctx := docsClient()
		if mode != config.ModeReadWrite {
			exitf("docs is configured as %s; change to readwrite with 'google-workspace config set --docs=readwrite' then re-authenticate", mode)
		}

		hasInsert := docsEditInsertText != ""
		hasReplace := docsEditFind != "" || docsEditReplaceWith != ""

		if !hasInsert && !hasReplace {
			exitf("specify one of: --insert-text or --find/--replace-with")
		}
		if hasInsert && hasReplace {
			exitf("specify only one operation mode per invocation")
		}

		if hasInsert {
			if err := client.InsertText(ctx, docsEditDocID, docsEditInsertText, docsEditIndex); err != nil {
				exitf("%v", err)
			}
			printJSON(map[string]string{"status": "ok", "operation": "insert"})
		} else {
			if docsEditFind == "" || docsEditReplaceWith == "" {
				exitf("both --find and --replace-with are required")
			}
			resp, err := client.ReplaceAllText(ctx, docsEditDocID, docsEditFind, docsEditReplaceWith)
			if err != nil {
				exitf("%v", err)
			}
			printJSON(resp)
		}
	},
}

func init() {
	docsReadCmd.Flags().StringVar(&docsReadDocID, "document-id", "", "document ID")

	docsEditCmd.Flags().StringVar(&docsEditDocID, "document-id", "", "document ID")
	docsEditCmd.Flags().StringVar(&docsEditInsertText, "insert-text", "", "text to insert")
	docsEditCmd.Flags().Int64Var(&docsEditIndex, "index", 0, "character index for insertion (0 = start of body)")
	docsEditCmd.Flags().StringVar(&docsEditFind, "find", "", "text to find (used with --replace-with)")
	docsEditCmd.Flags().StringVar(&docsEditReplaceWith, "replace-with", "", "replacement text (used with --find)")

	docsCmd.AddCommand(docsReadCmd, docsEditCmd)
	rootCmd.AddCommand(docsCmd)
}
