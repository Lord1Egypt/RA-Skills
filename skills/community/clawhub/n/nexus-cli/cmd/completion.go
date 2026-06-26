package cmd

import (
	"os"

	"github.com/spf13/cobra"
)

var completionCmd = &cobra.Command{
	Use:   "completion [bash|zsh|fish|powershell]",
	Short: "Generate shell completion scripts",
	Long: `Generate shell completion scripts for admirarr.

To load completions:

Bash:
  $ source <(admirarr completion bash)
  # To load completions for each session, execute once:
  $ admirarr completion bash > /etc/bash_completion.d/admirarr

Zsh:
  $ source <(admirarr completion zsh)
  # To load completions for each session, execute once:
  $ admirarr completion zsh > "${fpath[1]}/_admirarr"

Fish:
  $ admirarr completion fish | source
  # To load completions for each session, execute once:
  $ admirarr completion fish > ~/.config/fish/completions/admirarr.fish

PowerShell:
  PS> admirarr completion powershell | Out-String | Invoke-Expression`,
	DisableFlagsInUseLine: true,
	ValidArgs:             []string{"bash", "zsh", "fish", "powershell"},
	Args:                  cobra.MatchAll(cobra.ExactArgs(1), cobra.OnlyValidArgs),
	Run: func(cmd *cobra.Command, args []string) {
		switch args[0] {
		case "bash":
			_ = rootCmd.GenBashCompletion(os.Stdout)
		case "zsh":
			_ = rootCmd.GenZshCompletion(os.Stdout)
		case "fish":
			_ = rootCmd.GenFishCompletion(os.Stdout, true)
		case "powershell":
			_ = rootCmd.GenPowerShellCompletionWithDesc(os.Stdout)
		}
	},
}

func init() {
	rootCmd.AddCommand(completionCmd)
}
