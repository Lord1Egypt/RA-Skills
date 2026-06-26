package google

import (
	"context"
	"errors"
	"fmt"

	"github.com/PanthroCorp-Limited/openclaw-skills/google-workspace/internal/config"
	"golang.org/x/oauth2"
	"google.golang.org/api/calendar/v3"
	"google.golang.org/api/option"
)

// ErrReadOnly is returned when a write operation is attempted in readonly mode.
var ErrReadOnly = errors.New("calendar is configured as readonly; change to readwrite with 'google-workspace config set --calendar=readwrite' then re-authenticate")

// CalendarClient provides access to the Google Calendar API with
// configurable read/write mode.
type CalendarClient struct {
	svc  *calendar.Service
	mode config.CalendarMode
}

// NewCalendarClient creates a Calendar API client using the provided token source.
func NewCalendarClient(ctx context.Context, ts oauth2.TokenSource, mode config.CalendarMode) (*CalendarClient, error) {
	svc, err := calendar.NewService(ctx, option.WithTokenSource(ts))
	if err != nil {
		return nil, fmt.Errorf("creating calendar service: %w", err)
	}
	return &CalendarClient{svc: svc, mode: mode}, nil
}

// ListCalendars returns all calendars for the authenticated user.
func (c *CalendarClient) ListCalendars(ctx context.Context) ([]*calendar.CalendarListEntry, error) {
	resp, err := c.svc.CalendarList.List().Context(ctx).Do()
	if err != nil {
		return nil, fmt.Errorf("listing calendars: %w", err)
	}
	return resp.Items, nil
}

// ListEvents returns events within the specified time range.
func (c *CalendarClient) ListEvents(ctx context.Context, calendarID, timeMin, timeMax string, maxResults int64) ([]*calendar.Event, error) {
	call := c.svc.Events.List(calendarID).
		TimeMin(timeMin).
		TimeMax(timeMax).
		MaxResults(maxResults).
		SingleEvents(true).
		OrderBy("startTime").
		Context(ctx)

	resp, err := call.Do()
	if err != nil {
		return nil, fmt.Errorf("listing events: %w", err)
	}
	return resp.Items, nil
}

// GetEvent retrieves a single event by ID.
func (c *CalendarClient) GetEvent(ctx context.Context, calendarID, eventID string) (*calendar.Event, error) {
	event, err := c.svc.Events.Get(calendarID, eventID).Context(ctx).Do()
	if err != nil {
		return nil, fmt.Errorf("getting event %s: %w", eventID, err)
	}
	return event, nil
}

// CreateEvent creates a new calendar event. Requires readwrite mode.
func (c *CalendarClient) CreateEvent(ctx context.Context, calendarID string, event *calendar.Event) (*calendar.Event, error) {
	if c.mode != config.CalendarReadWrite {
		return nil, ErrReadOnly
	}
	created, err := c.svc.Events.Insert(calendarID, event).Context(ctx).Do()
	if err != nil {
		return nil, fmt.Errorf("creating event: %w", err)
	}
	return created, nil
}

// UpdateEvent updates an existing calendar event. Requires readwrite mode.
func (c *CalendarClient) UpdateEvent(ctx context.Context, calendarID, eventID string, event *calendar.Event) (*calendar.Event, error) {
	if c.mode != config.CalendarReadWrite {
		return nil, ErrReadOnly
	}
	updated, err := c.svc.Events.Update(calendarID, eventID, event).Context(ctx).Do()
	if err != nil {
		return nil, fmt.Errorf("updating event %s: %w", eventID, err)
	}
	return updated, nil
}

// DeleteEvent deletes a calendar event. Requires readwrite mode.
func (c *CalendarClient) DeleteEvent(ctx context.Context, calendarID, eventID string) error {
	if c.mode != config.CalendarReadWrite {
		return ErrReadOnly
	}
	if err := c.svc.Events.Delete(calendarID, eventID).Context(ctx).Do(); err != nil {
		return fmt.Errorf("deleting event %s: %w", eventID, err)
	}
	return nil
}
