package google

import (
	"context"
	"fmt"

	"golang.org/x/oauth2"
	"google.golang.org/api/option"
	"google.golang.org/api/people/v1"
)

// ContactsClient provides read-only access to the Google People API.
// No create, update, or delete operations exist in this type.
type ContactsClient struct {
	svc *people.Service
}

// NewContactsClient creates a People API client using the provided token source.
func NewContactsClient(ctx context.Context, ts oauth2.TokenSource) (*ContactsClient, error) {
	svc, err := people.NewService(ctx, option.WithTokenSource(ts))
	if err != nil {
		return nil, fmt.Errorf("creating people service: %w", err)
	}
	return &ContactsClient{svc: svc}, nil
}

// ListContacts returns contacts for the authenticated user.
func (c *ContactsClient) ListContacts(ctx context.Context, maxResults int64) ([]*people.Person, error) {
	call := c.svc.People.Connections.List("people/me").
		PersonFields("names,emailAddresses,phoneNumbers,organizations").
		PageSize(maxResults).
		Context(ctx)

	resp, err := call.Do()
	if err != nil {
		return nil, fmt.Errorf("listing contacts: %w", err)
	}
	return resp.Connections, nil
}

// SearchContacts searches for contacts matching the query.
func (c *ContactsClient) SearchContacts(ctx context.Context, query string, maxResults int64) ([]*people.Person, error) {
	call := c.svc.People.SearchContacts().
		Query(query).
		ReadMask("names,emailAddresses,phoneNumbers,organizations").
		PageSize(int64(maxResults)).
		Context(ctx)

	resp, err := call.Do()
	if err != nil {
		return nil, fmt.Errorf("searching contacts: %w", err)
	}

	var persons []*people.Person
	for _, result := range resp.Results {
		persons = append(persons, result.Person)
	}
	return persons, nil
}

// GetContact retrieves a single contact by resource name.
func (c *ContactsClient) GetContact(ctx context.Context, resourceName string) (*people.Person, error) {
	person, err := c.svc.People.Get(resourceName).
		PersonFields("names,emailAddresses,phoneNumbers,organizations,biographies").
		Context(ctx).Do()
	if err != nil {
		return nil, fmt.Errorf("getting contact %s: %w", resourceName, err)
	}
	return person, nil
}
