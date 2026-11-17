package cli

import (
	"fmt"

	"github.com/spf13/cobra"

	"github.com/stozo04/google-health-cli/internal/api"
)

// newTypesCmd exposes the embedded data-type catalog so agents can discover what
// is queryable without a network call.
func newTypesCmd(app *App) *cobra.Command {
	cmd := &cobra.Command{
		Use:   "types",
		Short: "Inspect the Google Health data types this tool can read",
		Args:  cobra.NoArgs,
		RunE: func(c *cobra.Command, _ []string) error {
			return c.Help()
		},
	}
	cmd.AddCommand(newTypesListCmd(app), newTypesDescribeCmd(app))
	return cmd
}

// typeView is the `types ... --json` shape: the catalog entry plus the derived
// read scope and a listable convenience flag. Key order is frozen.
type typeView struct {
	Name            string   `json:"name"`
	EndpointName    string   `json:"endpoint_name"`
	FilterName      string   `json:"filter_name"`
	RecordType      string   `json:"record_type"`
	Operations      []string `json:"operations"`
	Listable        bool     `json:"listable"`
	Scope           string   `json:"scope"`
	ReadScope       string   `json:"read_scope"`
	DefaultTimePath string   `json:"default_time_path"`
}

func toTypeView(dt api.DataType) typeView {
	return typeView{
		Name:            dt.Name,
		EndpointName:    dt.EndpointName,
		FilterName:      dt.FilterName,
		RecordType:      dt.RecordType,
		Operations:      dt.Operations,
		Listable:        dt.Supports("list"),
		Scope:           dt.Scope,
		ReadScope:       dt.ReadScope(),
		DefaultTimePath: dt.DefaultTimePath,
	}
}

func newTypesListCmd(_ *App) *cobra.Command {
	var asJSON bool
	cmd := &cobra.Command{
		Use:   "list",
		Short: "List every Google Health data type",
		Args:  cobra.NoArgs,
		RunE: func(cmd *cobra.Command, _ []string) error {
			types := api.DataTypes()
			out := cmd.OutOrStdout()
			if asJSON {
				views := make([]typeView, 0, len(types))
				for _, dt := range types {
					views = append(views, toTypeView(dt))
				}
				return writeJSON(out, views)
			}
			fprintf(out, "%d Google Health data types (* = supports list):\n\n", len(types))
			for _, dt := range types {
				mark := " "
				if dt.Supports("list") {
					mark = "*"
				}
				fprintf(out, "  %s %-32s %-8s %s\n", mark, dt.EndpointName, dt.RecordType, dt.Scope)
			}
			fprintln(cmd.ErrOrStderr(), "\nRead a type with:  google-health-cli data list <endpoint-name>")
			return nil
		},
	}
	cmd.Flags().BoolVar(&asJSON, "json", false, "machine-readable output")
	return cmd
}

func newTypesDescribeCmd(_ *App) *cobra.Command {
	var asJSON bool
	cmd := &cobra.Command{
		Use:   "describe <type>",
		Short: "Show one data type's record shape, scope, operations, and time path",
		Args:  cobra.ExactArgs(1),
		RunE: func(cmd *cobra.Command, args []string) error {
			dt, ok := api.LookupDataType(args[0])
			if !ok {
				return withCode(ExitUsage, fmt.Errorf(
					"unknown data type %q; run `google-health-cli types list`", args[0],
				))
			}
			view := toTypeView(dt)
			out := cmd.OutOrStdout()
			if asJSON {
				return writeJSON(out, view)
			}
			fprintf(out, "name:           %s\n", view.Name)
			fprintf(out, "endpoint_name:  %s\n", view.EndpointName)
			fprintf(out, "filter_name:    %s\n", view.FilterName)
			fprintf(out, "record_type:    %s\n", view.RecordType)
			fprintf(out, "operations:     %v\n", view.Operations)
			fprintf(out, "listable:       %t\n", view.Listable)
			fprintf(out, "scope:          %s\n", view.Scope)
			fprintf(out, "read_scope:     %s\n", view.ReadScope)
			fprintf(out, "time_path:      %s\n", view.DefaultTimePath)
			return nil
		},
	}
	cmd.Flags().BoolVar(&asJSON, "json", false, "machine-readable output")
	return cmd
}
