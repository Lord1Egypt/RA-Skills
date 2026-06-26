// NanoGPT API response types

export interface NanoGPTModel {
  id: string;
  provider: string;
  name: string;
  context_length: number;
  max_output_tokens: number;
  pricing: {
    prompt: number;   // $/million tokens
    completion: number;
  };
  capabilities: {
    vision?: boolean;
    reasoning?: boolean;
  };
}

export interface NanoGPTModelsResponse {
  models: NanoGPTModel[];
}


