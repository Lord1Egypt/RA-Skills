import { MAX_PAGE_SIZE } from './contract.mjs';

const SEARCH_CACHE_TTL_MS = 60_000;

function normalizeText(value) {
  return value.trim().toLowerCase();
}

function normalizeType(value) {
  return value.trim().toUpperCase();
}

function normalizeList(values, normalizer) {
  return [...new Set((values ?? []).map((value) => normalizer(String(value))).filter(Boolean))];
}

function requireAllowed(values, allowed, label) {
  for (const value of values) {
    if (!allowed.has(value)) {
      throw new Error(`Unsupported ${label} filter: ${value}.`);
    }
  }
}

function decodeCursor(cursor) {
  if (!cursor) {
    return 0;
  }

  const offset = Number.parseInt(cursor, 10);
  if (!Number.isFinite(offset) || offset < 0) {
    throw new Error('Cursor is invalid.');
  }

  return offset;
}

function buildCacheKey(input) {
  return JSON.stringify(input);
}

function getSearchText(lounge) {
  return [
    lounge.airportCode,
    lounge.airportName,
    lounge.country,
    lounge.city,
    lounge.type,
    lounge.terminal,
    lounge.name,
    lounge.location,
    ...(Array.isArray(lounge.facilities) ? lounge.facilities : []),
    ...(Array.isArray(lounge.conditions) ? lounge.conditions : []),
  ]
    .join(' ')
    .toLowerCase();
}

function toSummary(lounge) {
  return {
    id: lounge.id,
    airportCode: lounge.airportCode,
    airportName: lounge.airportName,
    country: lounge.country,
    city: lounge.city,
    type: lounge.type,
    terminal: lounge.terminal,
    name: lounge.name,
    facilities: lounge.facilities,
    location: lounge.location,
    lat: lounge.lat,
    lon: lounge.lon,
  };
}

function toDetail(lounge) {
  const { searchText, ...detail } = lounge;
  void searchText;
  return detail;
}

function scoreLounge(lounge, query, airportCode) {
  let score = 0;

  if (airportCode && lounge.airportCode === airportCode) {
    score += 400;
  }

  if (!query) {
    return score;
  }

  if (lounge.airportCode === query.toUpperCase()) {
    score += 250;
  }

  if (lounge.name.toLowerCase().includes(query)) {
    score += 120;
  }

  if (lounge.airportName.toLowerCase().includes(query)) {
    score += 80;
  }

  if (lounge.city.toLowerCase().includes(query)) {
    score += 60;
  }

  if (lounge.country.toLowerCase().includes(query)) {
    score += 40;
  }

  if (lounge.searchText.includes(query)) {
    score += 20;
  }

  return score;
}

function sortMatches(first, second) {
  return (
    second.score - first.score ||
    first.lounge.airportCode.localeCompare(second.lounge.airportCode) ||
    first.lounge.name.localeCompare(second.lounge.name)
  );
}

export function createCatalogStore(catalogData) {
  const catalog = {
    generatedAt: catalogData.generatedAt,
    sourceFile: catalogData.sourceFile,
    stats: catalogData.stats,
    filters: catalogData.filters,
    lounges: catalogData.lounges.map((lounge) => ({
      ...lounge,
      searchText: lounge.searchText ?? getSearchText(lounge),
    })),
  };
  const lounges = [...catalog.lounges];
  const loungeById = new Map(lounges.map((lounge) => [lounge.id, lounge]));
  const allowedTypes = new Set(catalog.filters.types);
  const allowedCountries = new Set(catalog.filters.countries);
  const allowedCities = new Set(catalog.filters.cities);
  const allowedFacilities = new Set(catalog.filters.facilities);
  const searchCache = new Map();

  function getCachedSearch(key) {
    const cached = searchCache.get(key);
    if (!cached) {
      return null;
    }

    if (Date.now() > cached.expiresAt) {
      searchCache.delete(key);
      return null;
    }

    return cached.value;
  }

  function setCachedSearch(key, value) {
    searchCache.set(key, {
      value,
      expiresAt: Date.now() + SEARCH_CACHE_TTL_MS,
    });
  }

  return {
    getCatalogMeta() {
      return {
        generatedAt: catalog.generatedAt,
        sourceFile: catalog.sourceFile,
        stats: catalog.stats,
        filters: catalog.filters,
      };
    },

    getFiltersResource() {
      return {
        stats: catalog.stats,
        filters: catalog.filters,
      };
    },

    getLoungeById(id) {
      const lounge = loungeById.get(id);
      return lounge ? toDetail(lounge) : null;
    },

    getAllLounges() {
      return lounges;
    },

    searchLounges(input) {
      const query = input.query ? normalizeText(input.query) : null;
      const airportCode = input.airportCode?.trim().toUpperCase() ?? null;
      const country = input.country?.trim() ?? null;
      const city = input.city?.trim() ?? null;
      const types = normalizeList(input.types, normalizeType);
      const facilities = normalizeList(input.facilities, (value) => value.trim());
      const limit = input.limit ?? 10;
      const offset = decodeCursor(input.cursor);

      if (limit > MAX_PAGE_SIZE) {
        throw new Error(`Limit must be ${MAX_PAGE_SIZE} or smaller.`);
      }

      if (country && !allowedCountries.has(country)) {
        throw new Error(`Unsupported country filter: ${country}.`);
      }

      if (city && !allowedCities.has(city)) {
        throw new Error(`Unsupported city filter: ${city}.`);
      }

      requireAllowed(types, allowedTypes, 'type');
      requireAllowed(facilities, allowedFacilities, 'facility');

      const cacheKey = buildCacheKey({
        query,
        airportCode,
        country,
        city,
        types,
        facilities,
        limit,
        offset,
      });
      const cached = getCachedSearch(cacheKey);
      if (cached) {
        return cached;
      }

      const matches = lounges
        .filter((lounge) => {
          if (airportCode && lounge.airportCode !== airportCode) {
            return false;
          }

          if (country && lounge.country !== country) {
            return false;
          }

          if (city && lounge.city !== city) {
            return false;
          }

          if (types.length > 0 && !types.includes(lounge.type)) {
            return false;
          }

          if (facilities.length > 0 && !facilities.every((facility) => lounge.facilities.includes(facility))) {
            return false;
          }

          if (query && !lounge.searchText.includes(query) && lounge.airportCode !== query.toUpperCase()) {
            return false;
          }

          return true;
        })
        .map((lounge) => ({
          lounge,
          score: scoreLounge(lounge, query, airportCode),
        }))
        .sort(sortMatches);

      const page = matches.slice(offset, offset + limit).map(({ lounge }) => toSummary(lounge));
      const result = {
        totalMatches: matches.length,
        nextCursor: offset + limit < matches.length ? String(offset + limit) : null,
        results: page,
      };

      setCachedSearch(cacheKey, result);
      return result;
    },
  };
}
