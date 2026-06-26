import { isRecord } from "../lib/config.ts";
import type { CommandDef } from "../lib/types.ts";
import { getNewApiErrorMessage } from "../lib/types.ts";

const VALID_MODES = ["DRIVE", "WALK", "BICYCLE", "TRANSIT"] as const;

function validateMode(value: string): string | null {
  if (!(VALID_MODES as readonly string[]).includes(value)) {
    return `must be one of ${VALID_MODES.join(", ")}`;
  }
  return null;
}

const directions: CommandDef = {
  name: "directions",
  description: "Compute routes between an origin and destination using the Routes API.",
  usage: "directions --origin <text> --dest <text> [--mode DRIVE|WALK|BICYCLE|TRANSIT]",
  method: "POST",
  url: "https://routes.googleapis.com/directions/v2:computeRoutes",
  auth: "header",
  fieldMask: "routes.duration,routes.distanceMeters,routes.polyline.encodedPolyline,routes.legs",
  flags: {
    origin: {
      description: "Origin address or lat,lng",
      required: true,
      placeholder: "<text>",
    },
    dest: {
      description: "Destination address or lat,lng",
      required: true,
      placeholder: "<text>",
    },
    mode: {
      description: "Travel mode",
      required: false,
      placeholder: "DRIVE|WALK|BICYCLE|TRANSIT",
      validate: validateMode,
    },
  },
  buildRequest: (flags) => ({
    body: {
      origin: { address: flags.origin },
      destination: { address: flags.dest },
      travelMode: flags.mode ?? "DRIVE",
    },
  }),
  checkSuccess: (httpStatus, payload) => {
    if (httpStatus < 200 || httpStatus >= 300) return false;
    if (!isRecord(payload)) return false;
    const routes = payload.routes;
    if (!Array.isArray(routes) || routes.length === 0) return false;
    return true;
  },
  getErrorMessage: (payload) => {
    if (isRecord(payload) && (!Array.isArray(payload.routes) || payload.routes.length === 0)) {
      return "No routes found. TRANSIT mode has limited regional coverage.";
    }
    return getNewApiErrorMessage(payload);
  },
};

export default directions;
