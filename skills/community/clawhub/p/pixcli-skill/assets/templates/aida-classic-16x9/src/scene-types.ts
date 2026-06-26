export type AidaStage = "attention" | "interest" | "desire" | "action";

export type AidaScene = {
  id: string;
  stage: AidaStage;
  durationInFrames: number;
  headline: string;
  subheadline?: string;
  voiceover: string;
  voiceoverFile?: string;
  sfxFile?: string;
  assetHint?: string;
};

export type AidaPlan = {
  productName: string;
  cta: string;
  incentive: string;
  musicFile?: string;
  scenes: AidaScene[];
};
