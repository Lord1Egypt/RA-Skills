import type { CommandDef } from "../lib/types.ts";
import { checkNewApiSuccess, getNewApiErrorMessage } from "../lib/types.ts";

function validateLocation(value: string): string | null {
  const parts = value.split(",");
  if (parts.length !== 2) {
    return "must be in <lat,lng> format";
  }
  const lat = Number(parts[0]?.trim());
  const lng = Number(parts[1]?.trim());
  if (!Number.isFinite(lat) || !Number.isFinite(lng)) {
    return "must contain valid numbers";
  }
  if (lat < -90 || lat > 90 || lng < -180 || lng > 180) {
    return "latitude must be -90..90, longitude must be -180..180";
  }
  return null;
}

function validateRadius(value: string): string | null {
  const num = Number(value);
  if (!Number.isFinite(num) || num <= 0) {
    return "must be a positive number (meters)";
  }
  return null;
}

const placesNearby: CommandDef = {
  name: "places-nearby",
  description: "Search for places near a location using the Places API (New).",
  usage: "places-nearby --location <lat,lng> --radius <meters> [--type <place_type>]",
  method: "POST",
  url: "https://places.googleapis.com/v1/places:searchNearby",
  auth: "header",
  fieldMask: "places.displayName,places.formattedAddress,places.id,places.location,places.rating,places.types",
  flags: {
    location: {
      description: "Center point for nearby search",
      required: true,
      placeholder: "<lat,lng>",
      validate: validateLocation,
    },
    radius: {
      description: "Search radius in meters",
      required: true,
      placeholder: "<meters>",
      validate: validateRadius,
    },
    type: {
      description: "Place type filter (e.g. restaurant, cafe, hotel)",
      required: false,
      placeholder: "<place_type>",
    },
  },
  buildRequest: (flags) => {
    const [lat, lng] = flags.location!.split(",").map(Number);

    const body: Record<string, unknown> = {
      locationRestriction: {
        circle: {
          center: { latitude: lat, longitude: lng },
          radius: Number(flags.radius),
        },
      },
    };

    if (flags.type) {
      body.includedTypes = [flags.type];
    }

    return { body };
  },
  checkSuccess: checkNewApiSuccess,
  getErrorMessage: getNewApiErrorMessage,
};

export default placesNearby;
