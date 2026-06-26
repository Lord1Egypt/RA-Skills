package cmd

import (
	"fmt"

	"github.com/spf13/cobra"
)

const Version = "0.0.1-dev"

var versionCmd = &cobra.Command{
	Use:   "version",
	Short: "Print nmail version",
	Run: func(cmd *cobra.Command, args []string) {
		fmt.Printf("nmail %s\n", Version)
	},
}
