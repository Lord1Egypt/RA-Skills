package cmd

import (
	"fmt"
	"time"

	imapclient "github.com/harlock/nmail/internal/imap"
	"github.com/harlock/nmail/internal/output"
	"github.com/spf13/cobra"
)

const dateLayout = "2006-01-02"

var searchCmd = &cobra.Command{
	Use:   "search",
	Short: "Search inbox messages",
	Long:  `Search inbox messages by sender, subject, text, date range, or unread status.`,
	RunE: func(cmd *cobra.Command, args []string) error {
		from, _ := cmd.Flags().GetString("from")
		subject, _ := cmd.Flags().GetString("subject")
		text, _ := cmd.Flags().GetString("text")
		sinceValue, _ := cmd.Flags().GetString("since")
		beforeValue, _ := cmd.Flags().GetString("before")
		unseen, _ := cmd.Flags().GetBool("unseen")
		limit, _ := cmd.Flags().GetInt("limit")
		accountEmail, _ := cmd.Flags().GetString("account")

		since, err := parseDateFlag(sinceValue)
		if err != nil {
			output.Error(err.Error())
			return nil
		}
		before, err := parseDateFlag(beforeValue)
		if err != nil {
			output.Error(err.Error())
			return nil
		}
		if limit < 0 {
			output.Error("--limit must be >= 0")
			return nil
		}

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

		msgs, err := cl.SearchMessages(imapclient.SearchQuery{
			From:    from,
			Subject: subject,
			Text:    text,
			Since:   since,
			Before:  before,
			Unseen:  unseen,
			Limit:   limit,
		})
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
			return nil
		}

		output.JSON(msgs)
		return nil
	},
}

func init() {
	searchCmd.Flags().String("from", "", "match sender")
	searchCmd.Flags().String("subject", "", "match subject")
	searchCmd.Flags().String("text", "", "match text in headers or body")
	searchCmd.Flags().String("since", "", "match messages on or after date (YYYY-MM-DD)")
	searchCmd.Flags().String("before", "", "match messages before date (YYYY-MM-DD)")
	searchCmd.Flags().Bool("unseen", false, "only include unread messages")
	searchCmd.Flags().Int("limit", 20, "maximum number of messages to return")
	searchCmd.Flags().String("account", "", "account email to use (default: first configured)")
}

func parseDateFlag(value string) (time.Time, error) {
	if value == "" {
		return time.Time{}, nil
	}

	parsed, err := time.Parse(dateLayout, value)
	if err != nil {
		return time.Time{}, fmt.Errorf("invalid date %q: expected YYYY-MM-DD", value)
	}
	return parsed, nil
}
