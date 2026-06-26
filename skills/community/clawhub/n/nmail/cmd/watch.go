package cmd

import (
	"context"
	"encoding/json"
	"fmt"
	"os"
	"os/signal"
	"syscall"
	"time"

	imapclient "github.com/harlock/nmail/internal/imap"
	"github.com/harlock/nmail/internal/output"
	"github.com/spf13/cobra"
)

const idleFallbackPollInterval = 5 * time.Second

var watchCmd = &cobra.Command{
	Use:   "watch",
	Short: "Watch inbox for new messages",
	Long:  `Watch INBOX for new messages using IMAP IDLE by default, or polling mode with --poll.`,
	RunE: func(cmd *cobra.Command, args []string) error {
		pollSeconds, _ := cmd.Flags().GetInt("poll")
		accountEmail, _ := cmd.Flags().GetString("account")
		if pollSeconds < 0 {
			output.Error("--poll must be >= 0")
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

		ctx, stop := signal.NotifyContext(context.Background(), os.Interrupt, syscall.SIGTERM)
		defer stop()

		handler := watchOutputHandler()
		if pollSeconds > 0 {
			err = cl.WatchPoll(ctx, time.Duration(pollSeconds)*time.Second, handler)
		} else {
			err = cl.Watch(ctx, idleFallbackPollInterval, handler)
		}
		if err != nil {
			output.Error(err.Error())
		}
		return nil
	},
}

func init() {
	watchCmd.Flags().Int("poll", 0, "poll every N seconds instead of using IMAP IDLE")
	watchCmd.Flags().String("account", "", "account email to use (default: first configured)")
}

func watchOutputHandler() func(imapclient.Message) error {
	if prettyOutput {
		return func(msg imapclient.Message) error {
			output.Pretty("📬 New: [%s] from %s", msg.Subject, msg.From)
			return nil
		}
	}

	enc := json.NewEncoder(os.Stdout)
	enc.SetEscapeHTML(false)
	return func(msg imapclient.Message) error {
		if err := enc.Encode(msg); err != nil {
			return fmt.Errorf("encoding message: %w", err)
		}
		return nil
	}
}
