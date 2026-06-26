export type ExplainerStage =
  | "context"
  | "problem"
  | "mechanism"
  | "benefits"
  | "next-step";

export type ExplainerScene = {
  id: string;
  stage: ExplainerStage;
  durationInFrames: number;
  headline: string;
  subheadline?: string;
  voiceover: string;
  voiceoverFile?: string;
  sfxFile?: string;
  assetHint?: string;
};

export type ExplainerPlan = {
  title: string;
  subtitle?: string;
  ctaText?: string;
  ctaUrl?: string;
  musicFile?: string;
  scenes: ExplainerScene[];
};
