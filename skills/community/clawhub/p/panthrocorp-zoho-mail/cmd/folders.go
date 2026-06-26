package cmd

import (
	"github.com/spf13/cobra"
)

var foldersCmd = &cobra.Command{
	Use:   "folders",
	Short: "Manage mail folders",
}

var foldersListCmd = &cobra.Command{
	Use:   "list",
	Short: "List all folders",
	Run: func(cmd *cobra.Command, args []string) {
		client, ctx := zohoClient()
		folders, err := client.ListFolders(ctx)
		if err != nil {
			exitf("%v", err)
		}
		printJSON(folders)
	},
}

func init() {
	foldersCmd.AddCommand(foldersListCmd)
	rootCmd.AddCommand(foldersCmd)
}
