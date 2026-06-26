import fs from 'node:fs/promises';
import path from 'node:path';

import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';

import {
  BrowserSearchPromptArgsSchema,
  LocalApiSurfaceResource,
  LocalHealthOutputSchema,
  ParseManualItineraryInputSchema,
  ParseMatrixLinkInputSchema,
  ParseStatusesResource,
  TravelerSafeAuditPromptArgsSchema,
  TripIdInputSchema,
} from './contract.mjs';
import { createMatrixMateClient, resolveSkillRoot } from './client.mjs';

function textContent(text) {
  return [{ type: 'text', text }];
}

function createPromptMessage(text) {
  return {
    role: 'user',
    content: {
      type: 'text',
      text,
    },
  };
}

function jsonResource(uri, payload) {
  return {
    contents: [
      {
        uri,
        mimeType: 'application/json',
        text: `${JSON.stringify(payload, null, 2)}\n`,
      },
    ],
  };
}

async function readExample(relativePath, skillRoot) {
  const fullPath = path.resolve(skillRoot, relativePath);
  return fs.readFile(fullPath, 'utf8');
}

function buildTripSummary(payload) {
  if (!payload || typeof payload !== 'object') {
    return 'Trip data returned.';
  }

  const slices = Array.isArray(payload.structured_itinerary?.slices) ? payload.structured_itinerary.slices.length : 0;
  const segments = Array.isArray(payload.structured_itinerary?.segments) ? payload.structured_itinerary.segments.length : 0;
  return `Trip ${payload.id} is ${payload.status} with ${slices} slice(s) and ${segments} segment(s).`;
}

function buildAuditFacts(payload) {
  const itinerary = payload?.structured_itinerary;
  const slices = Array.isArray(itinerary?.slices) ? itinerary.slices : [];
  const discrepancies = Array.isArray(payload?.discrepancies) ? payload.discrepancies : [];
  const truthRows = Array.isArray(payload?.traveler_truth_table) ? payload.traveler_truth_table : [];

  const routeSummary = slices.length
    ? slices
        .map((slice) => `${slice.origin.code}-${slice.destination.code}`)
        .join(', ')
    : 'unknown route';

  const discrepancyLines = discrepancies.length
    ? discrepancies
        .slice(0, 5)
        .map((item) => `- [${item.severity}] ${item.field}: ${item.message}`)
        .join('\n')
    : '- No discrepancies reported.';

  const truthLines = truthRows.length
    ? truthRows
        .slice(0, 6)
        .map((item) => `- ${item.concern}: ${item.value} (${item.scope})`)
        .join('\n')
    : '- No traveler truth-table rows returned.';

  return { routeSummary, discrepancyLines, truthLines };
}

export function createMatrixMateMcpServer({
  serverInfo = { name: 'matrix-mate-offline', version: '1.0.0' },
  client = createMatrixMateClient(),
  skillRoot = resolveSkillRoot(),
  serverFactory = (resolvedServerInfo) => new McpServer(resolvedServerInfo),
} = {}) {
  const server = serverFactory(serverInfo);

  server.registerTool(
    'check_local_health',
    {
      title: 'Check local Matrix Mate health',
      description: 'Confirm that the local Matrix Mate app is reachable before using parse tools.',
      outputSchema: LocalHealthOutputSchema,
    },
    async () => {
      try {
        const result = await client.checkLocalHealth();
        return {
          structuredContent: result,
          content: textContent(result.message),
        };
      } catch (error) {
        const message = error instanceof Error ? error.message : 'Local health check failed.';
        return {
          isError: true,
          content: textContent(message),
        };
      }
    },
  );

  server.registerTool(
    'parse_matrix_link',
    {
      title: 'Parse Matrix itinerary link',
      description: 'Send an ITA Matrix itinerary URL to the local Matrix Mate parser.',
      inputSchema: ParseMatrixLinkInputSchema,
    },
    async ({ matrixUrl }) => {
      try {
        const result = await client.parseMatrixLink(matrixUrl);
        if (!result.ok) {
          return {
            isError: true,
            content: textContent(result.payload?.error || result.text || `Parse failed with status ${result.status}.`),
          };
        }

        const responsePayload = result.payload;
        const summary = responsePayload?.id
          ? `Parsed Matrix link into trip ${responsePayload.id} with status ${responsePayload.status}.`
          : responsePayload?.fallback?.message || 'Matrix link parse completed.';

        return {
          structuredContent: responsePayload,
          content: textContent(summary),
        };
      } catch (error) {
        const message = error instanceof Error ? error.message : 'Matrix link parse failed.';
        return {
          isError: true,
          content: textContent(message),
        };
      }
    },
  );

  server.registerTool(
    'parse_manual_itinerary',
    {
      title: 'Parse manual itinerary payload',
      description: 'Send pasted ITA Matrix JSON and optional fare rules text to Matrix Mate.',
      inputSchema: ParseManualItineraryInputSchema,
    },
    async ({ itaJson, rulesBundle }) => {
      try {
        const result = await client.parseManualItinerary({ itaJson, rulesBundle });
        if (!result.ok) {
          return {
            isError: true,
            content: textContent(result.payload?.error || result.text || `Manual parse failed with status ${result.status}.`),
          };
        }

        return {
          structuredContent: result.payload,
          content: textContent(`Created trip ${result.payload.id} with status ${result.payload.status}.`),
        };
      } catch (error) {
        const message = error instanceof Error ? error.message : 'Manual itinerary parse failed.';
        return {
          isError: true,
          content: textContent(message),
        };
      }
    },
  );

  server.registerTool(
    'get_trip',
    {
      title: 'Get parsed trip',
      description: 'Fetch the structured trip output for an existing Matrix Mate trip id.',
      inputSchema: TripIdInputSchema,
    },
    async ({ id }) => {
      try {
        const result = await client.getTrip(id);
        if (!result.ok) {
          return {
            isError: true,
            content: textContent(result.payload?.error || result.text || `Trip lookup failed with status ${result.status}.`),
          };
        }

        return {
          structuredContent: result.payload,
          content: textContent(buildTripSummary(result.payload)),
        };
      } catch (error) {
        const message = error instanceof Error ? error.message : 'Trip lookup failed.';
        return {
          isError: true,
          content: textContent(message),
        };
      }
    },
  );

  server.registerTool(
    'export_trip',
    {
      title: 'Export trip summaries',
      description: 'Fetch traveler-facing and agent-facing export text for an existing trip.',
      inputSchema: TripIdInputSchema,
    },
    async ({ id }) => {
      try {
        const result = await client.exportTrip(id);
        if (!result.ok) {
          return {
            isError: true,
            content: textContent(result.payload?.error || result.text || `Trip export failed with status ${result.status}.`),
          };
        }

        return {
          structuredContent: result.payload,
          content: textContent(`Exported traveler and agent summaries for trip ${id}.`),
        };
      } catch (error) {
        const message = error instanceof Error ? error.message : 'Trip export failed.';
        return {
          isError: true,
          content: textContent(message),
        };
      }
    },
  );

  server.registerTool(
    'get_future_booking_intent',
    {
      title: 'Get future booking intent',
      description: 'Fetch Matrix Mate\'s future booking intent payload for a parsed trip.',
      inputSchema: TripIdInputSchema,
    },
    async ({ id }) => {
      try {
        const result = await client.getFutureBookingIntent(id);
        if (!result.ok) {
          return {
            isError: true,
            content: textContent(result.payload?.error || result.text || `Booking intent lookup failed with status ${result.status}.`),
          };
        }

        return {
          structuredContent: result.payload,
          content: textContent(`Fetched future booking intent for trip ${id}.`),
        };
      } catch (error) {
        const message = error instanceof Error ? error.message : 'Booking intent lookup failed.';
        return {
          isError: true,
          content: textContent(message),
        };
      }
    },
  );

  server.registerResource(
    'parse-statuses',
    'matrix-mate://parse-statuses',
    {
      title: 'Parse status reference',
      description: 'Reference meanings for Matrix Mate parse statuses.',
    },
    async () => jsonResource('matrix-mate://parse-statuses', ParseStatusesResource),
  );

  server.registerResource(
    'local-api-surface',
    'matrix-mate://local-api-surface',
    {
      title: 'Local API surface',
      description: 'Mapping between Matrix Mate MCP tools and local HTTP endpoints.',
    },
    async () => jsonResource('matrix-mate://local-api-surface', LocalApiSurfaceResource),
  );

  server.registerResource(
    'example-matrix-link',
    'matrix-mate://examples/matrix-link',
    {
      title: 'Example Matrix link',
      description: 'Bundled sample itinerary link for local testing.',
    },
    async () => {
      const text = await readExample(path.join('assets', 'examples', 'sample-link.txt'), skillRoot);
      return {
        contents: [
          {
            uri: 'matrix-mate://examples/matrix-link',
            mimeType: 'text/plain',
            text,
          },
        ],
      };
    },
  );

  server.registerResource(
    'example-manual-input',
    'matrix-mate://examples/manual-input',
    {
      title: 'Example manual parse payload',
      description: 'Bundled JSON and rules examples for the manual fallback flow.',
    },
    async () => {
      const [itaJson, rulesBundle] = await Promise.all([
        readExample(path.join('assets', 'examples', 'sample-ita.json'), skillRoot),
        readExample(path.join('assets', 'examples', 'sample-rules.txt'), skillRoot),
      ]);
      return jsonResource('matrix-mate://examples/manual-input', {
        ita_json: itaJson,
        rules_bundle: rulesBundle,
      });
    },
  );

  server.registerPrompt(
    'browser-search-to-parse',
    {
      title: 'Browser search to parse',
      description: 'Guide the browser-assisted ITA Matrix search flow before parsing in Matrix Mate.',
      argsSchema: BrowserSearchPromptArgsSchema,
    },
    async ({ tripRequest }) => ({
      description: 'Search ITA Matrix in the browser, then parse the resulting itinerary in Matrix Mate.',
      messages: [
        createPromptMessage(
          `Use browser automation to search ITA Matrix for this request: ${tripRequest}\n\nFollow this exact sequence:\n1. Open ITA Matrix.\n2. Fill the search based on the request.\n3. Submit the search and wait for a result or itinerary page with a usable itinerary/share link.\n4. Capture that link.\n5. Call the Matrix Mate MCP tool \`parse_matrix_link\` with the captured URL.\n6. If Matrix Mate cannot verify the result, ask the user for manual ITA JSON plus fare rules text instead of inventing certainty.\n\nStay read-only. Do not log in, attempt checkout, or promise CAPTCHA bypass.`,
        ),
      ],
    }),
  );

  server.registerPrompt(
    'traveler-safe-audit-brief',
    {
      title: 'Traveler-safe audit brief',
      description: 'Create a grounded audit summary for an existing Matrix Mate trip.',
      argsSchema: TravelerSafeAuditPromptArgsSchema,
    },
    async ({ tripId, focus }) => {
      const result = await client.getTrip(tripId);
      if (!result.ok || !result.payload) {
        return {
          description: `Trip ${tripId} could not be loaded`,
          messages: [createPromptMessage(`Trip ${tripId} could not be loaded from the local Matrix Mate app. Ask the user to retry after checking the trip id and local app health.`)],
        };
      }

      const facts = buildAuditFacts(result.payload);
      return {
        description: `Traveler-safe audit brief for trip ${tripId}`,
        messages: [
          createPromptMessage(
            `Summarize Matrix Mate trip ${tripId} for a traveler-safe audit.${focus ? ` Focus on: ${focus}.` : ''}\n\nStatus: ${result.payload.status}\nRoute: ${facts.routeSummary}\n\nDiscrepancies:\n${facts.discrepancyLines}\n\nTraveler truth table highlights:\n${facts.truthLines}\n\nOnly use these Matrix Mate facts. If the trip needs review, say so plainly.`,
          ),
        ],
      };
    },
  );

  return server;
}
