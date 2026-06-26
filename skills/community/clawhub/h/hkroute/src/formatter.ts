import type { DirectionsRoute } from "./directions.js";
import type { Route, RouteLeg, SuccessOutput, ErrorOutput, Output } from "./types.js";

const MAX_ROUTES = 4;

/**
 * Generate a signature string for a route based on its leg structure.
 * Two routes with the same signature are the same itinerary
 * (possibly at different departure times).
 */
function routeSignature(legs: RouteLeg[]): string {
  return legs
    .map((leg) => `${leg.type}:${leg.route_number ?? ""}:${leg.departure_stop ?? ""}:${leg.arrival_stop ?? ""}`)
    .join("|");
}

/**
 * Remove near-identical routes, keeping only the first (best) variant.
 * Must be called AFTER sorting so the kept route is the best-ranked.
 */
function deduplicateRoutes(routes: Route[]): Route[] {
  const seen = new Set<string>();
  return routes.filter((route) => {
    const sig = routeSignature(route.legs);
    if (seen.has(sig)) return false;
    seen.add(sig);
    return true;
  });
}

function markActionableLegs(route: Route): Route {
  let foundFirstBus = false;
  return {
    ...route,
    legs: route.legs.map((leg) => {
      if (!foundFirstBus && leg.type === "bus") {
        foundFirstBus = true;
        return { ...leg, actionable: true };
      }
      return leg;
    }),
  };
}

/**
 * Calculate minutes until the first bus of the first bus leg.
 * Returns 0 if first leg is walk/MTR or no bus legs exist.
 */
function calculateWaitTimeMin(legs: RouteLeg[]): number {
  const firstBusLeg = legs.find((leg) => leg.type === "bus");
  if (!firstBusLeg) return 0;

  // If we have real-time ETAs, use the first one
  if (firstBusLeg.eta_source === "realtime" && firstBusLeg.etas && firstBusLeg.etas.length > 0) {
    const etaTime = new Date(firstBusLeg.etas[0]).getTime();
    const now = Date.now();
    const minutes = Math.max(0, Math.round((etaTime - now) / 60000));
    return minutes;
  }

  // No real-time data — wait time is unknown, assume 0 (schedule-based)
  return 0;
}

export function formatRoutes(
  directionsRoutes: DirectionsRoute[],
  origin: string,
  destination: string,
): Output {
  if (directionsRoutes.length === 0) {
    return {
      error: true,
      code: "NO_TRANSIT_ROUTES",
      message:
        "No transit routes found. This may be due to the time of day or the locations provided. Consider trying a different departure time or checking if taxi is an option.",
    } satisfies ErrorOutput;
  }

  // Build Route objects with effective time calculations
  const routes: Route[] = directionsRoutes
    .map((dr) => {
      const waitTimeMin = calculateWaitTimeMin(dr.legs);
      const totalDurationMin = Math.round(dr.total_duration_seconds / 60);
      const effectiveTotalMin = waitTimeMin + totalDurationMin;

      return {
        rank: 0,
        recommended: false,
        total_duration_seconds: dr.total_duration_seconds,
        effective_duration_seconds: dr.total_duration_seconds,
        wait_time_min: waitTimeMin,
        effective_total_min: effectiveTotalMin,
        departure_time: dr.departure_time,
        arrival_time: dr.arrival_time,
        legs: dr.legs,
      };
    })
    .sort((a, b) => a.effective_total_min - b.effective_total_min);

  // Deduplicate after sorting so we keep the best variant of each itinerary
  const deduplicated = deduplicateRoutes(routes)
    .slice(0, MAX_ROUTES)
    .map((route, i) => markActionableLegs({ ...route, rank: i + 1, recommended: i === 0 }));

  return {
    error: false,
    origin,
    destination,
    queried_at: new Date().toISOString(),
    routes: deduplicated,
  } satisfies SuccessOutput;
}
