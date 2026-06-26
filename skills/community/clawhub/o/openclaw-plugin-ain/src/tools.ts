import { run, classifyTask, estimateComplexity } from '@felipematos/ain-cli';
import type { OpenClawPluginApi } from './types.js';

export function registerAinTools(api: OpenClawPluginApi): void {
  api.registerTool({
    name: 'ain_run',
    description: 'Execute an LLM prompt through AIN with provider routing and structured output support',
    parameters: {
      type: 'object',
      properties: {
        prompt: { type: 'string', description: 'The prompt to send to the LLM' },
        provider: { type: 'string', description: 'Provider name (optional)' },
        model: { type: 'string', description: 'Model ID or alias (optional)' },
        jsonMode: { type: 'boolean', description: 'Request JSON output' },
        schema: { type: 'object', description: 'JSON schema for structured output' },
        system: { type: 'string', description: 'System prompt' },
        temperature: { type: 'number', description: 'Temperature (0-2)' },
      },
      required: ['prompt'],
    },
    async execute(params) {
      const result = await run({
        prompt: params.prompt as string,
        provider: params.provider as string | undefined,
        model: params.model as string | undefined,
        jsonMode: params.jsonMode as boolean | undefined,
        schema: params.schema as object | undefined,
        system: params.system as string | undefined,
        temperature: params.temperature as number | undefined,
      });
      return {
        output: result.output,
        provider: result.provider,
        model: result.model,
        usage: result.usage,
        parsedOutput: result.parsedOutput,
      };
    },
  });

  api.registerTool({
    name: 'ain_classify',
    description: 'Classify a prompt by task type and estimate its complexity',
    parameters: {
      type: 'object',
      properties: {
        prompt: { type: 'string', description: 'The prompt to classify' },
      },
      required: ['prompt'],
    },
    async execute(params) {
      const prompt = params.prompt as string;
      return {
        taskType: classifyTask(prompt),
        complexity: estimateComplexity(prompt),
      };
    },
  });
}
