package cmd

import (
	"fmt"
	"strconv"

	imapclient "github.com/harlock/nmail/internal/imap"
	"github.com/harlock/nmail/internal/output"
	"github.com/spf13/cobra"
)

var readCmd = &cobra.Command{
	Use:   "read <id>",
	Short: "Read a message by ID",
	Args:  cobra.ExactArgs(1),
	RunE: func(cmd *cobra.Command, args []string) error {
		id, err := strconv.ParseUint(args[0], 10, 32)
		if err != nil {
			output.Error(fmt.Sprintf("invalid id: %s", args[0]))
			return nil
		}

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

		msg, err := cl.FetchMessage(uint32(id))
		if err != nil {
			output.Error(err.Error())
			return nil
		}

		if prettyOutput {
			output.Pretty("From:    %s", msg.From)
			output.Pretty("Subject: %s", msg.Subject)
			output.Pretty("Date:    %s", msg.Date.Format("2006-01-02 15:04:05"))
			output.Pretty("---")
			output.Pretty("%s", msg.Body)
		} else {
			output.JSON(msg)
		}
		return nil
	},
}

func init() {
	readCmd.Flags().String("account", "", "account email to use (default: first configured)")
}
