import { z } from 'zod';

export const MatrixUrlSchema = z
  .string()
  .trim()
  .url()
  .refine((value) => /matrix\.itasoftware\.com\/itinerary/u.test(value), 'Use an ITA Matrix itinerary URL.');

export const ParseMatrixLinkInputSchema = z
  .object({
    matrixUrl: MatrixUrlSchema,
  })
  .strict();

export const ParseManualItineraryInputSchema = z
  .object({
    itaJson: z.string().min(1),
    rulesBundle: z.string().optional(),
  })
  .strict();

export const TripIdInputSchema = z
  .object({
    id: z.string().trim().min(1).max(128),
  })
  .strict();

export const LocalHealthOutputSchema = z.object({
  ok: z.boolean(),
  baseUrl: z.string(),
  status: z.number().nullable(),
  titleDetected: z.boolean(),
  message: z.string(),
});

export const ParseStatusesResource = {
  statuses: [
    {
      name: 'verified',
      meaning: 'Matrix Mate reconciled itinerary and rules without blocking discrepancies.',
    },
    {
      name: 'needs_review',
      meaning: 'A blocking discrepancy exists and a human review is required.',
    },
    {
      name: 'draft_json_only',
      meaning: 'Only manual JSON was available, so rules coverage remains draft-grade.',
    },
  ],
};

export const LocalApiSurfaceResource = {
  tools: {
    parse_matrix_link: 'POST /v1/intake/matrix-link',
    parse_manual_itinerary: 'POST /v1/intake/ita',
    get_trip: 'GET /v1/trips/:id',
    export_trip: 'GET /v1/trips/:id/export',
    get_future_booking_intent: 'GET /v1/trips/:id/future-booking-intent',
    check_local_health: 'GET /',
  },
};

export const BrowserSearchPromptArgsSchema = {
  tripRequest: z.string().trim().min(1).max(800),
};

export const TravelerSafeAuditPromptArgsSchema = {
  tripId: z.string().trim().min(1).max(128),
  focus: z.string().trim().min(1).max(120).optional(),
};
