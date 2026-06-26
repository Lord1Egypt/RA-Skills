package cmd

import (
	"fmt"
	"io"
	"os"
	"strings"

	"github.com/harlock/nmail/internal/output"
	nmailsmtp "github.com/harlock/nmail/internal/smtp"
	"github.com/spf13/cobra"
)

var sendCmd = &cobra.Command{
	Use:   "send",
	Short: "Send an email",
	RunE: func(cmd *cobra.Command, args []string) error {
		to, _ := cmd.Flags().GetString("to")
		subject, _ := cmd.Flags().GetString("subject")
		body, _ := cmd.Flags().GetString("body")
		bodyFile, _ := cmd.Flags().GetString("body-file")

		// Read body from file if specified
		if bodyFile != "" {
			var data []byte
			var err error
			if bodyFile == "-" {
				data, err = io.ReadAll(os.Stdin)
			} else {
				data, err = os.ReadFile(bodyFile)
			}
			if err != nil {
				output.Error(fmt.Sprintf("reading body file: %v", err))
				return nil
			}
			body = string(data)
		}

		if strings.TrimSpace(body) == "" {
			output.Error("body is empty — use --body or --body-file")
			return nil
		}

		accountEmail, _ := cmd.Flags().GetString("account")
		account, err := resolveAccount(accountEmail)
		if err != nil {
			output.Error(err.Error())
			return nil
		}

		if err := nmailsmtp.Send(*account, to, subject, body); err != nil {
			output.Error(err.Error())
			return nil
		}

		if prettyOutput {
			output.Pretty("Sent to %s: %s", to, subject)
		} else {
			output.JSON(map[string]string{
				"status":  "sent",
				"to":      to,
				"subject": subject,
			})
		}
		return nil
	},
}

func init() {
	sendCmd.Flags().String("to", "", "recipient email address")
	sendCmd.Flags().String("subject", "", "email subject")
	sendCmd.Flags().String("body", "", "email body (plain text)")
	sendCmd.Flags().String("body-file", "", "read body from file (use - for stdin)")
	sendCmd.Flags().String("account", "", "account email to use (default: first configured)")

	sendCmd.MarkFlagRequired("to")
	sendCmd.MarkFlagRequired("subject")
}
