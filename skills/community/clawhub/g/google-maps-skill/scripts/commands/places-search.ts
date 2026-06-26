import type { CommandDef } from "../lib/types.ts";
import { checkNewApiSuccess, getNewApiErrorMessage } from "../lib/types.ts";

function validateRadius(value: string): string | null {
  const num = Number(value);
  if (!Number.isFinite(num) || num <= 0) {
    return "must be a positive number (meters)";
  }
  return null;
}

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

const placesSearch: CommandDef = {
  name: "places-search",
  description: "Search for places by text query using the Places API (New).",
  usage: "places-search --query <text> [--location <lat,lng>] [--radius <meters>]",
  method: "POST",
  url: "https://places.googleapis.com/v1/places:searchText",
  auth: "header",
  fieldMask: "places.displayName,places.formattedAddress,places.id,places.location,places.rating,places.types",
  flags: {
    query: {
      description: "Text query for place search",
      required: true,
      placeholder: "<text>",
    },
    location: {
      description: "Center point for location bias",
      required: false,
      placeholder: "<lat,lng>",
      validate: validateLocation,
    },
    radius: {
      description: "Radius in meters for location bias",
      required: false,
      placeholder: "<meters>",
      validate: validateRadius,
    },
  },
  buildRequest: (flags) => {
    const body: Record<string, unknown> = {
      textQuery: flags.query,
    };

    if (flags.location) {
      const [lat, lng] = flags.location.split(",").map(Number);
      const locationBias: Record<string, unknown> = {
        circle: {
          center: { latitude: lat, longitude: lng },
          radius: flags.radius ? Number(flags.radius) : 5000,
        },
      };
      body.locationBias = locationBias;
    }

    return { body };
  },
  checkSuccess: checkNewApiSuccess,
  getErrorMessage: getNewApiErrorMessage,
};

export default placesSearch;
