# Event Sources

User-listed sources are primary for their standard location. The agent may use other public sources for verification or one-off discovery, but should not add or log new primary-source suggestions during normal scans.

Replace the placeholder locations and sources with the user's actual locations and preferred event sources during setup.

## Standard Locations

The scanner can support any number of user-defined standard locations. There must always be at least one standard location.

The user defines standard locations and provides primary sources for them. Do not invent primary sources for a standard location.

Default location: <PLACEHOLDER>Example City.</PLACEHOLDER>

Current standard locations:
<PLACEHOLDER>
- Example City.
- Optional Second Location.
</PLACEHOLDER>

If the user does not specify a location when asking for suggestions, use the default location.

If the requested location has primary sources below, check those first. If the requested location has no primary sources, or is not a standard location yet, explore public event sources for that location and keep source links for every candidate.

<PLACEHOLDER>
## Example City

Primary sources:
| Name | URL | Type | Notes |
| --- | --- | --- | --- |
| Example Municipal Events | https://example.com/events | Public event listing | Replace with the user's preferred broad local event source. |
| Example Ticketing Search | https://example.com/search | Ticketing and event listing | Replace with a ticketing, community, venue, or event platform source scoped to this location. |
</PLACEHOLDER>

<PLACEHOLDER>
## Optional Second Location

Primary sources:

| Name | URL | Type | Notes |
| --- | --- | --- | --- |
| Example Second Location Events | https://example.com/second-location/events | Public event listing | Replace or delete this section depending on the user's setup. |
</PLACEHOLDER>

## Source Rules

- Resolve the requested location before discovery starts.
- Check primary sources for the requested location first when they exist.
- If no location is requested, use the default location.
- Preserve source links for every candidate event.
- Prefer public pages, public event listings, venue listings, newsletters, and ticketing pages.
- Check for new primary-source suggestions only after `event-scanner-add-to-calendar` is used. Send suggestions in chat only, and only when the added event came from a source not covered here.
