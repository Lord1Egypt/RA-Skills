import type { EtaDb, Company } from "hk-bus-eta";

export interface MatchResult {
  stopId: string;
  stopName: string;
  /** Distance in meters between Google's boarding coords and matched stop */
  distance: number;
}

/**
 * Map Google Maps agency names → hk-bus-eta company codes.
 * Google returns these as transit_details.line.agencies[0].name.
 */
const AGENCY_TO_COMPANY: Record<string, Company> = {
  // Major franchised bus operators
  "KMB": "kmb",
  "Kowloon Motor Bus": "kmb",
  "Citybus": "ctb",
  "Citybus Limited": "ctb",
  "CTB": "ctb",
  "New Lantao Bus": "nlb",
  "NLB": "nlb",
  // LRT feeder buses
  "LRT Feeder Bus": "lrtfeeder",
  // Green minibus
  "GMB": "gmb",
  "Green Minibus": "gmb",
  // Light Rail
  "Light Rail": "lightRail",
  "MTR Light Rail": "lightRail",
  // MTR (subway/heavy rail)
  "MTR": "mtr",
  "MTR Corporation": "mtr",
  // Ferries
  "Sun Ferry": "sunferry",
  "HKKF": "hkkf",
  "Hong Kong & Kowloon Ferry": "hkkf",
  "Fortune Ferry": "fortuneferry",
};

/** Maximum distance (meters) to consider a stop a valid match */
const MAX_MATCH_DISTANCE_M = 500;

/**
 * Map a Google Maps agency name to an hk-bus-eta company code.
 * Returns null for unknown agencies.
 */
export function mapAgency(agencyName: string): Company | null {
  // Try exact match first
  const exact = AGENCY_TO_COMPANY[agencyName];
  if (exact) return exact;

  // Try case-insensitive match
  const lower = agencyName.toLowerCase();
  for (const [key, value] of Object.entries(AGENCY_TO_COMPANY)) {
    if (key.toLowerCase() === lower) return value;
  }

  return null;
}

/**
 * Haversine distance between two points in meters.
 */
function haversineDistance(
  lat1: number,
  lng1: number,
  lat2: number,
  lng2: number,
): number {
  const R = 6371000; // Earth radius in meters
  const toRad = (deg: number) => (deg * Math.PI) / 180;
  const dLat = toRad(lat2 - lat1);
  const dLng = toRad(lng2 - lng1);
  const a =
    Math.sin(dLat / 2) ** 2 +
    Math.cos(toRad(lat1)) * Math.cos(toRad(lat2)) * Math.sin(dLng / 2) ** 2;
  return R * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
}

/**
 * Given a route number, operator name (from Google Maps), and boarding
 * coordinates, resolve the corresponding stop ID in the hk-bus-eta database.
 *
 * Three-step process:
 * 1. Map Google Maps agency name → hk-bus-eta company code
 * 2. Filter route database to stops on matching route + operator
 * 3. Find closest stop by geodesic distance to boarding coordinates
 *
 * Returns null if no match found (unknown agency, no matching route, or
 * no stop within MAX_MATCH_DISTANCE_M).
 */
export function matchStop(
  etaDb: EtaDb,
  routeNumber: string,
  googleAgencyName: string,
  boardingLat: number,
  boardingLng: number,
): MatchResult | null {
  // Step 1: Map agency name to company code
  const company = mapAgency(googleAgencyName);
  if (!company) {
    process.stderr.write(
      `[matcher] Unknown agency: "${googleAgencyName}" — falling back to schedule\n`,
    );
    return null;
  }

  // Step 2: Find route entries matching this operator + route number
  const candidateStopIds = new Set<string>();

  for (const key of Object.keys(etaDb.routeList)) {
    const entry = etaDb.routeList[key];
    if (entry.route !== routeNumber) continue;
    if (!entry.co.includes(company)) continue;

    const stops = entry.stops[company];
    if (stops) {
      for (const stopId of stops) {
        candidateStopIds.add(stopId);
      }
    }
  }

  if (candidateStopIds.size === 0) {
    return null;
  }

  // Step 3: Find closest stop by geodesic distance
  let bestStop: MatchResult | null = null;

  for (const stopId of candidateStopIds) {
    const stop = etaDb.stopList[stopId];
    if (!stop?.location) continue;

    const dist = haversineDistance(
      boardingLat,
      boardingLng,
      stop.location.lat,
      stop.location.lng,
    );

    if (dist <= MAX_MATCH_DISTANCE_M && (!bestStop || dist < bestStop.distance)) {
      bestStop = {
        stopId,
        stopName: stop.name.en,
        distance: Math.round(dist),
      };
    }
  }

  return bestStop;
}
