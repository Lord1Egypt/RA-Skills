package cmd

import (
	imapclient "github.com/harlock/nmail/internal/imap"
	"github.com/harlock/nmail/internal/output"
	"github.com/spf13/cobra"
)

var inboxCmd = &cobra.Command{
	Use:   "inbox",
	Short: "List inbox messages",
	Long:  `Fetch messages from inbox. Outputs JSON by default.`,
	RunE: func(cmd *cobra.Command, args []string) error {
		limit, _ := cmd.Flags().GetInt("limit")

		accountEmail, _ := cmd.Flags().GetString("account")
		account, err := resolveAccount(accountEmail)
		if err != nil {
			output.Error(err.Error())
			return nil
		}

		cl, err := imapclient.Connect(*account)
		if err != nil {
			output.Error(err.Error())
			return nil
		}
		defer cl.Close()

		msgs, err := cl.FetchInbox(limit)
		if err != nil {
			output.Error(err.Error())
			return nil
		}

		if prettyOutput {
			if len(msgs) == 0 {
				output.Pretty("No messages.")
				return nil
			}
			for _, m := range msgs {
				read := " "
				if !m.IsRead {
					read = "●"
				}
				output.Pretty("[%d] %s %-40s %s", m.ID, read, m.Subject, m.From)
			}
		} else {
			output.JSON(msgs)
		}
		return nil
	},
}

func init() {
	inboxCmd.Flags().Int("limit", 20, "number of messages to fetch")
	inboxCmd.Flags().String("account", "", "account email to use (default: first configured)")
}
