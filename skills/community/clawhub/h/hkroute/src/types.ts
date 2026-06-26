export type LegType = "bus" | "mtr" | "walk" | "ferry" | "light_rail" | "tram" | "other";

export type EtaSource = "schedule" | "realtime" | "unavailable";

export interface RouteLeg {
  type: LegType;
  /** e.g. "6X", "M+", "968" */
  route_number: string | null;
  /** e.g. "KMB", "Citybus" */
  operator: string | null;
  departure_stop: string | null;
  arrival_stop: string | null;
  departure_location: { lat: number; lng: number } | null;
  arrival_location: { lat: number; lng: number } | null;
  duration_seconds: number;
  /** Number of stops on this leg */
  num_stops: number | null;
  /** Walking instructions or transit headsign */
  instructions: string | null;
  eta_source: EtaSource;
  /** Whether this is the first bus leg (the one that determines when you leave) */
  actionable: boolean;
  /** Real-time ETAs if available */
  etas: string[] | null;
}

export interface Route {
  rank: number;
  recommended: boolean;
  total_duration_seconds: number;
  effective_duration_seconds: number;
  /** Minutes until first bus of the first bus leg (0 if first leg is walk/MTR) */
  wait_time_min: number;
  /** wait_time_min + total_duration_min — used as ranking key */
  effective_total_min: number;
  departure_time: string | null;
  arrival_time: string | null;
  legs: RouteLeg[];
}

export interface SuccessOutput {
  error: false;
  origin: string;
  destination: string;
  queried_at: string;
  routes: Route[];
}

export interface ErrorOutput {
  error: true;
  code: "NO_TRANSIT_ROUTES" | "GOOGLE_API_ERROR" | "INVALID_INPUT";
  message: string;
}

export type Output = SuccessOutput | ErrorOutput;
