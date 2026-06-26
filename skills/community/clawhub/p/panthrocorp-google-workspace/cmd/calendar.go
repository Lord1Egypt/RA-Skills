package cmd

import (
	"context"
	"fmt"
	"time"

	"github.com/PanthroCorp-Limited/openclaw-skills/google-workspace/internal/config"
	gw "github.com/PanthroCorp-Limited/openclaw-skills/google-workspace/internal/google"
	"github.com/PanthroCorp-Limited/openclaw-skills/google-workspace/internal/oauth"
	"github.com/spf13/cobra"
	"google.golang.org/api/calendar/v3"
)

var calendarCmd = &cobra.Command{
	Use:   "calendar",
	Short: "Google Calendar operations",
}

func calendarClient() (*gw.CalendarClient, config.CalendarMode, context.Context) {
	ctx := context.Background()
	key := encryptionKey()
	if key == "" {
		exitf("GOOGLE_WORKSPACE_TOKEN_KEY is not set")
	}

	cfg, err := config.Load(configDir)
	if err != nil {
		exitf("loading config: %v", err)
	}
	if cfg.Calendar == config.CalendarOff {
		exitf("calendar is disabled in config; run 'google-workspace config set --calendar=readonly'")
	}

	token, err := oauth.LoadToken(configDir, key)
	if err != nil {
		exitf("%v", err)
	}

	oauthCfg := oauth.NewOAuthConfig(clientID(), clientSecret(), cfg.OAuthScopes())
	ts := oauthCfg.TokenSource(ctx, token)

	client, err := gw.NewCalendarClient(ctx, ts, cfg.Calendar)
	if err != nil {
		exitf("creating calendar client: %v", err)
	}
	return client, cfg.Calendar, ctx
}

var calendarListCmd = &cobra.Command{
	Use:   "list",
	Short: "List all calendars",
	Run: func(cmd *cobra.Command, args []string) {
		client, _, ctx := calendarClient()
		calendars, err := client.ListCalendars(ctx)
		if err != nil {
			exitf("%v", err)
		}
		printJSON(calendars)
	},
}

var (
	calEventsCalID      string
	calEventsFrom       string
	calEventsTo         string
	calEventsMaxResults int64
)

var calendarEventsCmd = &cobra.Command{
	Use:   "events",
	Short: "List calendar events within a date range",
	Run: func(cmd *cobra.Command, args []string) {
		client, _, ctx := calendarClient()

		timeMin := calEventsFrom
		if timeMin == "" {
			timeMin = time.Now().Format(time.RFC3339)
		}
		timeMax := calEventsTo
		if timeMax == "" {
			timeMax = time.Now().Add(7 * 24 * time.Hour).Format(time.RFC3339)
		}

		events, err := client.ListEvents(ctx, calEventsCalID, timeMin, timeMax, calEventsMaxResults)
		if err != nil {
			exitf("%v", err)
		}
		printJSON(events)
	},
}

var (
	calEventCalID string
	calEventID    string
)

var calendarEventCmd = &cobra.Command{
	Use:   "event",
	Short: "Get a single calendar event by ID",
	Run: func(cmd *cobra.Command, args []string) {
		if calEventID == "" {
			exitf("--id is required")
		}
		client, _, ctx := calendarClient()
		event, err := client.GetEvent(ctx, calEventCalID, calEventID)
		if err != nil {
			exitf("%v", err)
		}
		printJSON(event)
	},
}

var (
	calCreateCalID   string
	calCreateSummary string
	calCreateStart   string
	calCreateEnd     string
	calCreateDesc    string
)

var calendarCreateCmd = &cobra.Command{
	Use:   "create",
	Short: "Create a calendar event (requires readwrite mode)",
	Run: func(cmd *cobra.Command, args []string) {
		client, mode, ctx := calendarClient()
		if mode != config.CalendarReadWrite {
			exitf("calendar is in %s mode; change to readwrite to create events", mode)
		}

		event := &calendar.Event{
			Summary:     calCreateSummary,
			Description: calCreateDesc,
			Start:       &calendar.EventDateTime{DateTime: calCreateStart},
			End:         &calendar.EventDateTime{DateTime: calCreateEnd},
		}

		created, err := client.CreateEvent(ctx, calCreateCalID, event)
		if err != nil {
			exitf("%v", err)
		}
		printJSON(created)
	},
}

var (
	calUpdateCalID   string
	calUpdateID      string
	calUpdateSummary string
	calUpdateStart   string
	calUpdateEnd     string
	calUpdateDesc    string
)

var calendarUpdateCmd = &cobra.Command{
	Use:   "update",
	Short: "Update a calendar event (requires readwrite mode)",
	Run: func(cmd *cobra.Command, args []string) {
		if calUpdateID == "" {
			exitf("--id is required")
		}
		client, mode, ctx := calendarClient()
		if mode != config.CalendarReadWrite {
			exitf("calendar is in %s mode; change to readwrite to update events", mode)
		}

		event := &calendar.Event{}
		if calUpdateSummary != "" {
			event.Summary = calUpdateSummary
		}
		if calUpdateDesc != "" {
			event.Description = calUpdateDesc
		}
		if calUpdateStart != "" {
			event.Start = &calendar.EventDateTime{DateTime: calUpdateStart}
		}
		if calUpdateEnd != "" {
			event.End = &calendar.EventDateTime{DateTime: calUpdateEnd}
		}

		updated, err := client.UpdateEvent(ctx, calUpdateCalID, calUpdateID, event)
		if err != nil {
			exitf("%v", err)
		}
		printJSON(updated)
	},
}

var (
	calDeleteCalID string
	calDeleteID    string
)

var calendarDeleteCmd = &cobra.Command{
	Use:   "delete",
	Short: "Delete a calendar event (requires readwrite mode)",
	Run: func(cmd *cobra.Command, args []string) {
		if calDeleteID == "" {
			exitf("--id is required")
		}
		client, mode, ctx := calendarClient()
		if mode != config.CalendarReadWrite {
			exitf("calendar is in %s mode; change to readwrite to delete events", mode)
		}

		if err := client.DeleteEvent(ctx, calDeleteCalID, calDeleteID); err != nil {
			exitf("%v", err)
		}
		fmt.Println("Event deleted.")
	},
}

func init() {
	calendarEventsCmd.Flags().StringVar(&calEventsCalID, "calendar-id", "primary", "calendar ID")
	calendarEventsCmd.Flags().StringVar(&calEventsFrom, "from", "", "start time (RFC3339, defaults to now)")
	calendarEventsCmd.Flags().StringVar(&calEventsTo, "to", "", "end time (RFC3339, defaults to 7 days from now)")
	calendarEventsCmd.Flags().Int64Var(&calEventsMaxResults, "max-results", 25, "maximum number of results")

	calendarEventCmd.Flags().StringVar(&calEventCalID, "calendar-id", "primary", "calendar ID")
	calendarEventCmd.Flags().StringVar(&calEventID, "id", "", "event ID")

	calendarCreateCmd.Flags().StringVar(&calCreateCalID, "calendar-id", "primary", "calendar ID")
	calendarCreateCmd.Flags().StringVar(&calCreateSummary, "summary", "", "event title")
	calendarCreateCmd.Flags().StringVar(&calCreateStart, "start", "", "start time (RFC3339)")
	calendarCreateCmd.Flags().StringVar(&calCreateEnd, "end", "", "end time (RFC3339)")
	calendarCreateCmd.Flags().StringVar(&calCreateDesc, "description", "", "event description")

	calendarUpdateCmd.Flags().StringVar(&calUpdateCalID, "calendar-id", "primary", "calendar ID")
	calendarUpdateCmd.Flags().StringVar(&calUpdateID, "id", "", "event ID")
	calendarUpdateCmd.Flags().StringVar(&calUpdateSummary, "summary", "", "new event title")
	calendarUpdateCmd.Flags().StringVar(&calUpdateStart, "start", "", "new start time (RFC3339)")
	calendarUpdateCmd.Flags().StringVar(&calUpdateEnd, "end", "", "new end time (RFC3339)")
	calendarUpdateCmd.Flags().StringVar(&calUpdateDesc, "description", "", "new event description")

	calendarDeleteCmd.Flags().StringVar(&calDeleteCalID, "calendar-id", "primary", "calendar ID")
	calendarDeleteCmd.Flags().StringVar(&calDeleteID, "id", "", "event ID to delete")

	calendarCmd.AddCommand(calendarListCmd, calendarEventsCmd, calendarEventCmd, calendarCreateCmd, calendarUpdateCmd, calendarDeleteCmd)
	rootCmd.AddCommand(calendarCmd)
}
