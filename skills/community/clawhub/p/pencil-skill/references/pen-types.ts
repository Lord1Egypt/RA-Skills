// TypeScript definitions for .pen format (derived from pen-schema.json)

// Note: Schema _PRIVATE node types (e.g. `connection`) are intentionally excluded from the
// public authoring node union (`PenNodeType`). Top-level _PRIVATE keys (`fonts`, `imports`)
// are kept as optional fields on `PenDocument` for schema completeness, but agents should
// treat them as Pencil-internal metadata and avoid authoring them directly.
export const PEN_SCHEMA_VERSION = '2.8' as const;

export type PenNodeType =
  | 'rectangle'
  | 'ellipse'
  | 'line'
  | 'polygon'
  | 'path'
  | 'text'
  | 'frame'
  | 'group'
  | 'note'
  | 'prompt'
  | 'context'
  | 'icon_font'
  | 'ref';

export type Theme = Record<string, string>;
export type VariableRef = `$${string}`;
export type NumberOrVariable = number | VariableRef;
export type StringOrVariable = string | VariableRef;
export type BooleanOrVariable = boolean | VariableRef;
export type ColorOrVariable = ColorHex | VariableRef;

export interface ThemedValue<T> {
  value: T;
  theme?: Theme;
}

export type PenVariable =
  | { type: 'boolean'; value: BooleanOrVariable | ThemedValue<BooleanOrVariable>[] }
  | { type: 'color'; value: ColorOrVariable | ThemedValue<ColorOrVariable>[] }
  | { type: 'number'; value: NumberOrVariable | ThemedValue<NumberOrVariable>[] }
  | { type: 'string'; value: StringOrVariable | ThemedValue<StringOrVariable>[] };

export type ColorHex = `#${string}`;

export interface FillColor {
  type: 'color';
  enabled?: BooleanOrVariable;
  blendMode?: BlendMode;
  color: ColorOrVariable;
}

export interface GradientStop {
  color: ColorOrVariable;
  position: NumberOrVariable;
}

export interface FillGradient {
  type: 'gradient';
  enabled?: BooleanOrVariable;
  blendMode?: BlendMode;
  gradientType?: 'linear' | 'radial' | 'angular';
  opacity?: NumberOrVariable;
  center?: { x?: number; y?: number };
  size?: { width?: NumberOrVariable; height?: NumberOrVariable };
  rotation?: NumberOrVariable;
  colors?: GradientStop[];
}

export interface FillImage {
  type: 'image';
  enabled?: BooleanOrVariable;
  blendMode?: BlendMode;
  opacity?: NumberOrVariable;
  url: string;
  mode?: 'stretch' | 'fill' | 'fit';
}

export type MeshPoint =
  | [number, number]
  | {
      position: [number, number];
      leftHandle?: [number, number];
      rightHandle?: [number, number];
      topHandle?: [number, number];
      bottomHandle?: [number, number];
    };

export interface FillMeshGradient {
  type: 'mesh_gradient';
  enabled?: BooleanOrVariable;
  blendMode?: BlendMode;
  opacity?: NumberOrVariable;
  columns?: number;
  rows?: number;
  colors?: ColorOrVariable[];
  points?: MeshPoint[];
}

export type Fill = ColorOrVariable | FillColor | FillGradient | FillImage | FillMeshGradient;

export interface Stroke {
  align?: 'inside' | 'center' | 'outside';
  thickness?:
    | NumberOrVariable
    | {
        top?: NumberOrVariable;
        right?: NumberOrVariable;
        bottom?: NumberOrVariable;
        left?: NumberOrVariable;
      };
  join?: 'miter' | 'bevel' | 'round';
  miterAngle?: NumberOrVariable;
  cap?: 'none' | 'round' | 'square';
  dashPattern?: number[];
  fill?: Fill | Fill[];
}

export interface BlurEffect {
  type: 'blur' | 'background_blur';
  enabled?: BooleanOrVariable;
  radius?: NumberOrVariable;
}

export interface ShadowEffect {
  type: 'shadow';
  enabled?: BooleanOrVariable;
  shadowType?: 'inner' | 'outer';
  offset?: { x: NumberOrVariable; y: NumberOrVariable };
  spread?: NumberOrVariable;
  blur?: NumberOrVariable;
  color?: ColorOrVariable;
  blendMode?: BlendMode;
}

export type Effect = BlurEffect | ShadowEffect;

export interface TextStyle {
  fontFamily?: StringOrVariable;
  fontSize?: NumberOrVariable;
  fontWeight?: StringOrVariable;
  letterSpacing?: NumberOrVariable;
  fontStyle?: StringOrVariable;
  underline?: BooleanOrVariable;
  lineHeight?: NumberOrVariable;
  textAlign?: 'left' | 'center' | 'right' | 'justify';
  textAlignVertical?: 'top' | 'middle' | 'bottom';
  strikethrough?: BooleanOrVariable;
  href?: string;
}

export interface LayoutProps {
  layout?: 'none' | 'vertical' | 'horizontal';
  gap?: NumberOrVariable;
  layoutIncludeStroke?: boolean;
  padding?:
    | NumberOrVariable
    | [NumberOrVariable, NumberOrVariable]
    | [NumberOrVariable, NumberOrVariable, NumberOrVariable, NumberOrVariable];
  justifyContent?: 'start' | 'center' | 'end' | 'space_between' | 'space_around';
  alignItems?: 'start' | 'center' | 'end';
}

export interface PenNode extends LayoutProps {
  id: string;
  type: PenNodeType;
  name?: string;
  children?: PenNode[];
  x?: number;
  y?: number;
  width?: number | NumberOrVariable | 'fit_content' | 'fill_container' | `${'fit_content' | 'fill_container'}(${number})`;
  height?: number | NumberOrVariable | 'fit_content' | 'fill_container' | `${'fit_content' | 'fill_container'}(${number})`;
  opacity?: NumberOrVariable;
  enabled?: BooleanOrVariable;
  rotation?: NumberOrVariable;
  flipX?: BooleanOrVariable;
  flipY?: BooleanOrVariable;
  cornerRadius?: NumberOrVariable | [NumberOrVariable, NumberOrVariable, NumberOrVariable, NumberOrVariable];
  fill?: Fill | Fill[];
  stroke?: Stroke | Stroke[];
  effect?: Effect | Effect[];
  theme?: Theme;
  reusable?: boolean;
  ref?: string;
  descendants?: Record<string, Partial<PenNode>>;
  content?: string | Array<{ content?: string } & TextStyle>;
  textGrowth?: 'auto' | 'fixed-width' | 'fixed-width-height';
  clip?: BooleanOrVariable;
  slot?: string[];
  metadata?: { type: string; [key: string]: unknown };
  [key: string]: unknown;
}

export interface PenFontAxis {
  tag: string;
  start: number;
  end: number;
}

export interface PenFont {
  name?: string;
  url?: string;
  style?: 'normal' | 'italic';
  weight?: number | [number, number];
  axes?: PenFontAxis[];
}

export type BlendMode =
  | 'normal'
  | 'darken'
  | 'multiply'
  | 'linearBurn'
  | 'colorBurn'
  | 'light'
  | 'screen'
  | 'linearDodge'
  | 'colorDodge'
  | 'overlay'
  | 'softLight'
  | 'hardLight'
  | 'difference'
  | 'exclusion'
  | 'hue'
  | 'saturation'
  | 'color'
  | 'luminosity';

export interface PenDocument {
  version: typeof PEN_SCHEMA_VERSION;
  themes?: Record<string, string[]>;
  variables?: Record<string, PenVariable>;
  children: PenNode[];
  fonts?: PenFont[];
  imports?: Record<string, string>;
}
