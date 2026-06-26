# Basic Usage Example

This example demonstrates how to create a simple animated video using Remotion Video Skill.

## Quick Start

### 1. Install Dependencies
```bash
cd /Users/leo/Work/Skills/remotion-video-skill
npm install
```

### 2. Start Remotion Studio
```bash
npm run studio
```

### 3. Create Your First Video

Create a new file `src/compositions/MyFirstVideo.tsx`:

```typescript
import React from 'react';
import { AbsoluteFill, useCurrentFrame, interpolate } from 'remotion';
import { FadeIn, SlideIn, ScaleIn } from '../components';

export const MyFirstVideo: React.FC = () => {
  const frame = useCurrentFrame();

  return (
    <AbsoluteFill
      style={{
        backgroundColor: '#1a1a2e',
        justifyContent: 'center',
        alignItems: 'center',
      }}
    >
      {/* Animated title */}
      <FadeIn durationInFrames={30}>
        <SlideIn direction="top" durationInFrames={30}>
          <h1
            style={{
              fontSize: 80,
              color: '#e94560',
              fontFamily: 'Arial, sans-serif',
            }}
          >
            Hello Remotion!
          </h1>
        </SlideIn>
      </FadeIn>

      {/* Animated subtitle */}
      <FadeIn delayInFrames={30} durationInFrames={30}>
        <ScaleIn durationInFrames={30}>
          <p
            style={{
              fontSize: 32,
              color: '#ffffff',
              marginTop: 20,
            }}
          >
            Creating videos with code
          </p>
        </ScaleIn>
      </FadeIn>
    </AbsoluteFill>
  );
};
```

### 4. Register in Root.tsx

Add to `src/Root.tsx`:

```typescript
import { MyFirstVideo } from './compositions/MyFirstVideo';

// Inside the return statement:
<Composition
  id="MyFirstVideo"
  component={MyFirstVideo}
  durationInFrames={150}
  fps={30}
  width={1920}
  height={1080}
/>
```

### 5. Render to Video

```bash
npx remotion render MyFirstVideo out/my-first-video.mp4
```

## Component Usage Examples

### FadeIn
```typescript
<FadeIn durationInFrames={30} delayInFrames={0}>
  <div>Your content here</div>
</FadeIn>
```

### SlideIn (4 directions)
```typescript
<SlideIn direction="left" durationInFrames={30}>
  <div>Slides from left</div>
</SlideIn>

<SlideIn direction="right" durationInFrames={30}>
  <div>Slides from right</div>
</SlideIn>

<SlideIn direction="top" durationInFrames={30}>
  <div>Slides from top</div>
</SlideIn>

<SlideIn direction="bottom" durationInFrames={30}>
  <div>Slides from bottom</div>
</SlideIn>
```

### ScaleIn with Spring
```typescript
<ScaleIn durationInFrames={30} springPreset="bouncy">
  <div>Pops in with bounce effect</div>
</ScaleIn>
```

### Typewriter Effect
```typescript
<Typewriter
  text="This text appears character by character"
  durationInFrames={60}
  startFrame={0}
/>
```

### Word Highlight
```typescript
<WordHighlight
  text="Important words will be highlighted"
  highlightWords={['Important', 'highlighted']}
  durationInFrames={90}
/>
```
