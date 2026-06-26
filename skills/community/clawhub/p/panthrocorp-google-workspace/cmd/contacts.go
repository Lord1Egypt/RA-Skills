package cmd

import (
	"context"

	"github.com/PanthroCorp-Limited/openclaw-skills/google-workspace/internal/config"
	gw "github.com/PanthroCorp-Limited/openclaw-skills/google-workspace/internal/google"
	"github.com/PanthroCorp-Limited/openclaw-skills/google-workspace/internal/oauth"
	"github.com/spf13/cobra"
)

var contactsCmd = &cobra.Command{
	Use:   "contacts",
	Short: "Read-only Google Contacts operations",
}

func contactsClient() (*gw.ContactsClient, context.Context) {
	ctx := context.Background()
	key := encryptionKey()
	if key == "" {
		exitf("GOOGLE_WORKSPACE_TOKEN_KEY is not set")
	}

	cfg, err := config.Load(configDir)
	if err != nil {
		exitf("loading config: %v", err)
	}
	if !cfg.Contacts {
		exitf("contacts is disabled in config; run 'google-workspace config set --contacts=true'")
	}

	token, err := oauth.LoadToken(configDir, key)
	if err != nil {
		exitf("%v", err)
	}

	oauthCfg := oauth.NewOAuthConfig(clientID(), clientSecret(), cfg.OAuthScopes())
	ts := oauthCfg.TokenSource(ctx, token)

	client, err := gw.NewContactsClient(ctx, ts)
	if err != nil {
		exitf("creating contacts client: %v", err)
	}
	return client, ctx
}

var contactsListMaxResults int64

var contactsListCmd = &cobra.Command{
	Use:   "list",
	Short: "List contacts",
	Run: func(cmd *cobra.Command, args []string) {
		client, ctx := contactsClient()
		contacts, err := client.ListContacts(ctx, contactsListMaxResults)
		if err != nil {
			exitf("%v", err)
		}
		printJSON(contacts)
	},
}

var (
	contactsSearchQuery      string
	contactsSearchMaxResults int64
)

var contactsSearchCmd = &cobra.Command{
	Use:   "search",
	Short: "Search contacts by name or email",
	Run: func(cmd *cobra.Command, args []string) {
		if contactsSearchQuery == "" {
			exitf("--query is required")
		}
		client, ctx := contactsClient()
		contacts, err := client.SearchContacts(ctx, contactsSearchQuery, contactsSearchMaxResults)
		if err != nil {
			exitf("%v", err)
		}
		printJSON(contacts)
	},
}

var contactsGetResource string

var contactsGetCmd = &cobra.Command{
	Use:   "get",
	Short: "Get a single contact by resource name",
	Run: func(cmd *cobra.Command, args []string) {
		if contactsGetResource == "" {
			exitf("--id is required")
		}
		client, ctx := contactsClient()
		contact, err := client.GetContact(ctx, contactsGetResource)
		if err != nil {
			exitf("%v", err)
		}
		printJSON(contact)
	},
}

func init() {
	contactsListCmd.Flags().Int64Var(&contactsListMaxResults, "max-results", 100, "maximum number of contacts")

	contactsSearchCmd.Flags().StringVar(&contactsSearchQuery, "query", "", "search query")
	contactsSearchCmd.Flags().Int64Var(&contactsSearchMaxResults, "max-results", 10, "maximum number of results")

	contactsGetCmd.Flags().StringVar(&contactsGetResource, "id", "", "contact resource name (e.g. people/c1234)")

	contactsCmd.AddCommand(contactsListCmd, contactsSearchCmd, contactsGetCmd)
	rootCmd.AddCommand(contactsCmd)
}
