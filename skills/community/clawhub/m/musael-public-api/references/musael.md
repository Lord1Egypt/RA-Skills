# Musael endpoint reference

**Live as of October 23, 2026.** The endpoint is deployed.

- Method and route: GET https://musael.com/api/public/v1/names
- Optional query parameters: kind (default fantasy), seed (1-999999, default 1), count (1-20, default 10)
- Response fields: version "1", kind, seed, names, source
- Source page: https://musael.com/tools/{kind}-name-generator

Supported kinds:

    fantasy, fantasy-last, elf, dwarf, dragon, kingdom, town, village,
    tavern, wizard, orc, city, guild, ship, sword, spell, god, demon,
    vampire, pirate, knight, sci-fi-planet, alien, starship

The same kind and seed reproduce the same list for a given generator release. A future release may change its tables or behavior. Shared error and rate-limit rules are in [the API docs](../../../docs/api.md).
