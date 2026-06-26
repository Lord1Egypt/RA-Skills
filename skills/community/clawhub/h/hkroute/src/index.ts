import { getDirections } from "./directions.js";
import type { DirectionsRoute } from "./directions.js";
import { formatRoutes } from "./formatter.js";
import { loadEtaDb, getRealtimeEta } from "./eta.js";
import { matchStop, mapAgency } from "./matcher.js";
import type { ErrorOutput, RouteLeg, EtaSource } from "./types.js";

function parseArgs(args: string[]): {
  origin: string | null;
  destination: string | null;
  departureTime: string | null;
} {
  const result: { origin: string | null; destination: string | null; departureTime: string | null } = {
    origin: null,
    destination: null,
    departureTime: null,
  };

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    if (arg === "--origin" && i + 1 < args.length) {
      result.origin = args[++i];
    } else if (arg === "--destination" && i + 1 < args.length) {
      result.destination = args[++i];
    } else if (arg === "--departure-time" && i + 1 < args.length) {
      result.departureTime = args[++i];
    }
  }

  return result;
}

const COORD_RE = /^-?\d+(\.\d+)?\s*,\s*-?\d+(\.\d+)?$/;

/** Append ", Hong Kong" to text inputs so Google can geocode ambiguous names like "Stanley". */
function qualifyLocation(input: string): string {
  if (COORD_RE.test(input)) return input;
  if (/hong\s*kong/i.test(input)) return input;
  return `${input}, Hong Kong`;
}

function exitWithError(code: ErrorOutput["code"], message: string): never {
  const output: ErrorOutput = { error: true, code, message };
  console.log(JSON.stringify(output, null, 2));
  return process.exit(1) as never;
}

/** Enrich bus/transit legs with real-time ETAs via matcher + ETA module */
async function enrichRoutes(routes: DirectionsRoute[]): Promise<DirectionsRoute[]> {
  const etaDb = await loadEtaDb();

  const enriched = await Promise.all(
    routes.map(async (route) => {
      const enrichedLegs = await Promise.all(
        route.legs.map(async (leg) => {
          // Only enrich transit legs that have a route number and operator
          if (leg.type === "walk" || !leg.route_number || !leg.operator || !leg.departure_location) {
            return leg;
          }

          // MTR/subway: skip ETA enrichment (high frequency)
          const company = mapAgency(leg.operator);
          if (!company || company === "mtr") {
            return leg;
          }

          // Step 1: Match the Google Maps stop to an hk-bus-eta stop ID
          const match = matchStop(
            etaDb,
            leg.route_number,
            leg.operator,
            leg.departure_location.lat,
            leg.departure_location.lng,
          );

          if (!match) {
            // Unmatched route → keep schedule data
            return leg;
          }

          // Step 2: Fetch real-time ETA for the matched stop
          const etas = await getRealtimeEta(etaDb, company, leg.route_number, match.stopId);

          if (etas === null) {
            // Operator skipped (e.g. MTR) — shouldn't reach here but handle gracefully
            return leg;
          }

          if (etas.length === 0) {
            // ETA unavailable (late night, no service, etc.)
            return {
              ...leg,
              eta_source: "unavailable" as EtaSource,
              etas: [],
            };
          }

          // Enrich with real-time data
          return {
            ...leg,
            eta_source: "realtime" as EtaSource,
            etas: etas.map((e) => e.eta),
          };
        }),
      );

      return { ...route, legs: enrichedLegs };
    }),
  );

  return enriched;
}

async function main() {
  const { origin, destination, departureTime } = parseArgs(process.argv.slice(2));

  if (!origin || !destination) {
    return exitWithError("INVALID_INPUT", "Both --origin and --destination are required.");
  }

  const apiKey = process.env.GOOGLE_MAPS_API_KEY;
  if (!apiKey) {
    return exitWithError("INVALID_INPUT", "GOOGLE_MAPS_API_KEY environment variable is not set.");
  }

  let departureDate: Date | undefined;
  if (departureTime) {
    departureDate = new Date(departureTime);
    if (isNaN(departureDate.getTime())) {
      return exitWithError("INVALID_INPUT", `Invalid departure time: "${departureTime}". Use ISO 8601 format.`);
    }
  }

  try {
    const routes = await getDirections(qualifyLocation(origin), qualifyLocation(destination), apiKey, departureDate);

    // Enrich bus legs with real-time ETAs (matcher + ETA module)
    let enrichedRoutes = routes;
    try {
      enrichedRoutes = await enrichRoutes(routes);
    } catch (err) {
      // ETA enrichment failure is non-fatal — fall back to schedule data
      process.stderr.write(
        `[eta] Enrichment failed, using schedule data: ${err instanceof Error ? err.message : String(err)}\n`,
      );
    }

    const output = formatRoutes(enrichedRoutes, origin, destination);
    console.log(JSON.stringify(output, null, 2));

    if (output.error) {
      process.exit(1);
    }
  } catch (err) {
    const message = err instanceof Error ? err.message : String(err);
    exitWithError("GOOGLE_API_ERROR", message);
  }
}

main();
