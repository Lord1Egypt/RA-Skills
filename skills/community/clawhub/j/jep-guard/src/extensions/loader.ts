import { Extension, ExtensionResult, ExecutionRequest, GuardContext } from '../core/types';

export class ExtensionLoaderService {
  private extensions = new Map<string, Extension>();
  private context: GuardContext;

  constructor(ctx: GuardContext) {
    this.context = ctx;
  }

  async loadBuiltins(): Promise<void> {
    // Optional integrations require explicit, reviewed adapters. No mutable global hooks.

  }

  async evaluateAll(request: ExecutionRequest): Promise<ExtensionResult[]> {
    const results: ExtensionResult[] = [];
    for (const [name, ext] of this.extensions) {
      if (ext.evaluate) {
        const res = await ext.evaluate(request);
        results.push({ ...res, extension: name });
      }
    }
    return results;
  }

  get(name: string): Extension | undefined {
    return this.extensions.get(name);
  }

  getReputation(skillId: string) {
    return this.context.reputation.get(skillId);
  }
}