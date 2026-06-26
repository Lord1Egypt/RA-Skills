import {
  Client,
  TravelMode,
  VehicleType,
} from "@googlemaps/google-maps-services-js";
import type { LegType, RouteLeg } from "./types.js";

const client = new Client({});

export interface DirectionsRoute {
  total_duration_seconds: number;
  departure_time: string | null;
  arrival_time: string | null;
  legs: RouteLeg[];
}

function classifyVehicle(vehicleType: VehicleType | undefined): LegType {
  switch (vehicleType) {
    case VehicleType.BUS:
    case VehicleType.INTERCITY_BUS:
    case VehicleType.TROLLEYBUS:
    case VehicleType.SHARE_TAXI:
      return "bus";
    case VehicleType.SUBWAY:
    case VehicleType.HEAVY_RAIL:
      return "mtr";
    case VehicleType.TRAM:
      return "tram";
    case VehicleType.METRO_RAIL:
    case VehicleType.RAIL:
    case VehicleType.COMMUTER_TRAIN:
    case VehicleType.MONORAIL:
      return "light_rail";
    case VehicleType.FERRY:
      return "ferry";
    default:
      return "other";
  }
}

export async function getDirections(
  origin: string,
  destination: string,
  apiKey: string,
  departureTime?: Date,
): Promise<DirectionsRoute[]> {
  const response = await client.directions({
    params: {
      origin,
      destination,
      mode: TravelMode.transit,
      alternatives: true,
      departure_time: departureTime ?? "now",
      region: "hk",
      key: apiKey,
    },
  });

  const data = response.data;

  if (data.status === "ZERO_RESULTS") {
    return [];
  }

  if (data.status !== "OK") {
    throw new Error(`Google Maps API error: ${data.status} — ${data.error_message ?? "unknown"}`);
  }

  return data.routes.map((route) => {
    // Google returns a single leg for transit directions (origin → destination)
    // but that leg contains multiple steps (walk, bus, walk, mtr, walk, etc.)
    const googleLeg = route.legs[0];

    const legs: RouteLeg[] = googleLeg.steps.map((step) => {
      if (String(step.travel_mode).toLowerCase() === TravelMode.walking) {
        return {
          type: "walk" as LegType,
          route_number: null,
          operator: null,
          departure_stop: null,
          arrival_stop: null,
          departure_location: step.start_location
            ? { lat: step.start_location.lat, lng: step.start_location.lng }
            : null,
          arrival_location: step.end_location
            ? { lat: step.end_location.lat, lng: step.end_location.lng }
            : null,
          duration_seconds: step.duration?.value ?? 0,
          num_stops: null,
          instructions: step.html_instructions?.replace(/<[^>]*>/g, "") ?? null,
          eta_source: "schedule" as const,
          actionable: false,
          etas: null,
        };
      }

      // Transit step
      const transit = step.transit_details;
      const vehicleType = transit?.line?.vehicle?.type;
      const legType = classifyVehicle(vehicleType);

      return {
        type: legType,
        route_number: transit?.line?.short_name ?? transit?.line?.name ?? null,
        operator: transit?.line?.agencies?.[0]?.name ?? null,
        departure_stop: transit?.departure_stop?.name ?? null,
        arrival_stop: transit?.arrival_stop?.name ?? null,
        departure_location: transit?.departure_stop?.location
          ? {
              lat: transit.departure_stop.location.lat,
              lng: transit.departure_stop.location.lng,
            }
          : null,
        arrival_location: transit?.arrival_stop?.location
          ? {
              lat: transit.arrival_stop.location.lat,
              lng: transit.arrival_stop.location.lng,
            }
          : null,
        duration_seconds: step.duration?.value ?? 0,
        num_stops: transit?.num_stops ?? null,
        instructions: transit?.headsign ? `Towards ${transit.headsign}` : null,
        eta_source: "schedule" as const,
        actionable: false,
        etas: null,
      };
    });

    return {
      total_duration_seconds: googleLeg.duration?.value ?? 0,
      departure_time: googleLeg.departure_time?.text ?? null,
      arrival_time: googleLeg.arrival_time?.text ?? null,
      legs,
    };
  });
}
