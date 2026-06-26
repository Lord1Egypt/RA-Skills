import { BailianEngine } from './bailian';
import { TavilyEngine } from './tavily';
import { SerperEngine } from './serper';
import { ExaEngine } from './exa';
import { FirecrawlEngine } from './firecrawl';

export { BailianEngine, TavilyEngine, SerperEngine, ExaEngine, FirecrawlEngine };

export function getEngine(name: string) {
  switch (name) {
    case 'bailian':
      return new BailianEngine();
    case 'tavily':
      return new TavilyEngine();
    case 'serper':
      return new SerperEngine();
    case 'exa':
      return new ExaEngine();
    case 'firecrawl':
      return new FirecrawlEngine();
    default:
      throw new Error(`Unknown engine: ${name}`);
  }
}

export function getAllEngines() {
  return [
    new BailianEngine(),
    new TavilyEngine(),
    new SerperEngine(),
    new ExaEngine(),
    new FirecrawlEngine()
  ];
}