package cmd

import (
	"context"
	"encoding/json"

	"github.com/PanthroCorp-Limited/openclaw-skills/google-workspace/internal/config"
	gw "github.com/PanthroCorp-Limited/openclaw-skills/google-workspace/internal/google"
	"github.com/PanthroCorp-Limited/openclaw-skills/google-workspace/internal/oauth"
	"github.com/spf13/cobra"
)

var sheetsCmd = &cobra.Command{
	Use:   "sheets",
	Short: "Google Sheets operations",
}

func sheetsClient() (*gw.SheetsClient, config.ServiceMode, context.Context) {
	ctx := context.Background()
	key := encryptionKey()
	if key == "" {
		exitf("GOOGLE_WORKSPACE_TOKEN_KEY is not set")
	}

	cfg, err := config.Load(configDir)
	if err != nil {
		exitf("loading config: %v", err)
	}
	if cfg.Sheets == config.ModeOff {
		exitf("sheets is disabled in config; run 'google-workspace config set --sheets=readonly'")
	}

	token, err := oauth.LoadToken(configDir, key)
	if err != nil {
		exitf("%v", err)
	}

	oauthCfg := oauth.NewOAuthConfig(clientID(), clientSecret(), cfg.OAuthScopes())
	ts := oauthCfg.TokenSource(ctx, token)

	client, err := gw.NewSheetsClient(ctx, ts, cfg.Sheets)
	if err != nil {
		exitf("creating sheets client: %v", err)
	}
	return client, cfg.Sheets, ctx
}

var sheetsListSpreadsheetID string

var sheetsListCmd = &cobra.Command{
	Use:   "list",
	Short: "List sheets in a spreadsheet",
	Run: func(cmd *cobra.Command, args []string) {
		if sheetsListSpreadsheetID == "" {
			exitf("--spreadsheet-id is required")
		}
		client, _, ctx := sheetsClient()
		ss, err := client.GetSpreadsheet(ctx, sheetsListSpreadsheetID)
		if err != nil {
			exitf("%v", err)
		}
		printJSON(ss)
	},
}

var (
	sheetsReadSpreadsheetID string
	sheetsReadRange         string
)

var sheetsReadCmd = &cobra.Command{
	Use:   "read",
	Short: "Read cell values from a range",
	Run: func(cmd *cobra.Command, args []string) {
		if sheetsReadSpreadsheetID == "" {
			exitf("--spreadsheet-id is required")
		}
		if sheetsReadRange == "" {
			exitf("--range is required")
		}
		client, _, ctx := sheetsClient()
		vr, err := client.ReadRange(ctx, sheetsReadSpreadsheetID, sheetsReadRange)
		if err != nil {
			exitf("%v", err)
		}
		printJSON(vr)
	},
}

var (
	sheetsWriteSpreadsheetID string
	sheetsWriteRange         string
	sheetsWriteValues        string
	sheetsWriteRaw           bool
)

var sheetsWriteCmd = &cobra.Command{
	Use:   "write",
	Short: "Write cell values to a range (requires readwrite mode)",
	Run: func(cmd *cobra.Command, args []string) {
		if sheetsWriteSpreadsheetID == "" {
			exitf("--spreadsheet-id is required")
		}
		if sheetsWriteRange == "" {
			exitf("--range is required")
		}
		if sheetsWriteValues == "" {
			exitf("--values is required")
		}

		client, mode, ctx := sheetsClient()
		if mode != config.ModeReadWrite {
			exitf("sheets is configured as %s; change to readwrite with 'google-workspace config set --sheets=readwrite' then re-authenticate", mode)
		}

		var values [][]interface{}
		if err := json.Unmarshal([]byte(sheetsWriteValues), &values); err != nil {
			exitf("parsing --values JSON: %v", err)
		}

		if err := client.WriteRange(ctx, sheetsWriteSpreadsheetID, sheetsWriteRange, values, sheetsWriteRaw); err != nil {
			exitf("%v", err)
		}
		printJSON(map[string]string{"status": "ok", "operation": "write"})
	},
}

func init() {
	sheetsListCmd.Flags().StringVar(&sheetsListSpreadsheetID, "spreadsheet-id", "", "spreadsheet ID")

	sheetsReadCmd.Flags().StringVar(&sheetsReadSpreadsheetID, "spreadsheet-id", "", "spreadsheet ID")
	sheetsReadCmd.Flags().StringVar(&sheetsReadRange, "range", "", "A1-notation range (e.g. Sheet1!A1:C10)")

	sheetsWriteCmd.Flags().StringVar(&sheetsWriteSpreadsheetID, "spreadsheet-id", "", "spreadsheet ID")
	sheetsWriteCmd.Flags().StringVar(&sheetsWriteRange, "range", "", "A1-notation range (e.g. Sheet1!A1:C3)")
	sheetsWriteCmd.Flags().StringVar(&sheetsWriteValues, "values", "", "JSON 2D array (e.g. [[\"a\",\"b\"],[\"c\",\"d\"]])")
	sheetsWriteCmd.Flags().BoolVar(&sheetsWriteRaw, "raw", false, "store values as-is without formula evaluation")

	sheetsCmd.AddCommand(sheetsListCmd, sheetsReadCmd, sheetsWriteCmd)
	rootCmd.AddCommand(sheetsCmd)
}
