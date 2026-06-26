# Title Animation Example

This example shows how to create cinematic title animations.

## Title Sequence Styles

### 1. Cinematic Style
Dramatic, movie-like title with slow reveals.

```typescript
import React from 'react';
import { AbsoluteFill, useCurrentFrame, interpolate, spring } from 'remotion';
import { FadeIn, ScaleIn } from '../components';

export const CinematicTitle: React.FC = () => {
  const frame = useCurrentFrame();

  return (
    <AbsoluteFill
      style={{
        backgroundColor: '#000000',
        justifyContent: 'center',
        alignItems: 'center',
      }}
    >
      <FadeIn durationInFrames={60}>
        <ScaleIn durationInFrames={90} springPreset="gentle">
          <h1
            style={{
              fontSize: 120,
              color: '#ffffff',
              fontFamily: 'Georgia, serif',
              letterSpacing: 20,
              textTransform: 'uppercase',
            }}
          >
            CINEMATIC
          </h1>
        </ScaleIn>
      </FadeIn>

      <FadeIn delayInFrames={60} durationInFrames={45}>
        <p
          style={{
            fontSize: 24,
            color: '#888888',
            fontFamily: 'Georgia, serif',
            letterSpacing: 10,
            textTransform: 'uppercase',
          }}
        >
          A Story Begins
        </p>
      </FadeIn>
    </AbsoluteFill>
  );
};
```

### 2. Minimal Style
Clean, simple title with subtle animations.

```typescript
import React from 'react';
import { AbsoluteFill } from 'remotion';
import { FadeIn, SlideIn } from '../components';

export const MinimalTitle: React.FC = () => {
  return (
    <AbsoluteFill
      style={{
        backgroundColor: '#ffffff',
        justifyContent: 'center',
        alignItems: 'center',
      }}
    >
      <FadeIn durationInFrames={30}>
        <h1
          style={{
            fontSize: 72,
            color: '#000000',
            fontFamily: 'Helvetica, sans-serif',
            fontWeight: 300,
          }}
        >
          Minimal Design
        </h1>
      </FadeIn>

      <SlideIn direction="left" delayInFrames={30} durationInFrames={30}>
        <div
          style={{
            width: 60,
            height: 2,
            backgroundColor: '#000000',
            marginTop: 20,
          }}
        />
      </SlideIn>
    </AbsoluteFill>
  );
};
```

### 3. Playful Style
Fun, energetic title with bouncy animations.

```typescript
import React from 'react';
import { AbsoluteFill, useCurrentFrame, spring } from 'remotion';
import { ScaleIn, FadeIn } from '../components';

export const PlayfulTitle: React.FC = () => {
  const frame = useCurrentFrame();
  const words = ['Hello', 'World', '!'];

  return (
    <AbsoluteFill
      style={{
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        justifyContent: 'center',
        alignItems: 'center',
        flexDirection: 'row',
        gap: 20,
      }}
    >
      {words.map((word, index) => (
        <ScaleIn
          key={index}
          delayInFrames={index * 10}
          durationInFrames={30}
          springPreset="bouncy"
        >
          <span
            style={{
              fontSize: 80,
              color: '#ffffff',
              fontFamily: 'Comic Sans MS, cursive',
            }}
          >
            {word}
          </span>
        </ScaleIn>
      ))}
    </AbsoluteFill>
  );
};
```

### 4. Corporate Style
Professional, business-appropriate title.

```typescript
import React from 'react';
import { AbsoluteFill } from 'remotion';
import { FadeIn, SlideIn } from '../components';

export const CorporateTitle: React.FC = () => {
  return (
    <AbsoluteFill
      style={{
        backgroundColor: '#1a365d',
        justifyContent: 'center',
        alignItems: 'center',
      }}
    >
      <FadeIn durationInFrames={30}>
        <SlideIn direction="top" durationInFrames={30}>
          <h1
            style={{
              fontSize: 64,
              color: '#ffffff',
              fontFamily: 'Arial, sans-serif',
              fontWeight: 600,
            }}
          >
            Q4 Financial Report
          </h1>
        </SlideIn>
      </FadeIn>

      <FadeIn delayInFrames={30} durationInFrames={30}>
        <SlideIn direction="bottom" durationInFrames={30}>
          <p
            style={{
              fontSize: 28,
              color: '#90cdf4',
              fontFamily: 'Arial, sans-serif',
            }}
          >
            Annual Performance Review
          </p>
        </SlideIn>
      </FadeIn>
    </AbsoluteFill>
  );
};
```

## Staggered Text Animation

Create a title where each letter animates individually:

```typescript
import React from 'react';
import { AbsoluteFill, useCurrentFrame, spring, useVideoConfig } from 'remotion';

interface StaggeredTextProps {
  text: string;
  delayPerLetter?: number;
}

export const StaggeredText: React.FC<StaggeredTextProps> = ({
  text,
  delayPerLetter = 5
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  return (
    <AbsoluteFill
      style={{
        justifyContent: 'center',
        alignItems: 'center',
        flexDirection: 'row',
      }}
    >
      {text.split('').map((char, index) => {
        const delay = index * delayPerLetter;
        const progress = spring({
          frame: frame - delay,
          fps,
          config: {
            damping: 12,
            stiffness: 200,
            mass: 0.5,
          },
        });

        return (
          <span
            key={index}
            style={{
              fontSize: 80,
              color: '#ffffff',
              transform: `scale(${progress})`,
              opacity: progress,
              display: 'inline-block',
            }}
          >
            {char === ' ' ? '\u00A0' : char}
          </span>
        );
      })}
    </AbsoluteFill>
  );
};
```

## Usage

```typescript
// Register in Root.tsx
<Composition
  id="CinematicTitle"
  component={CinematicTitle}
  durationInFrames={150}
  fps={30}
  width={1920}
  height={1080}
/>
```
