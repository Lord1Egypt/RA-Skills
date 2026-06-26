export interface Goals {
  calories_kcal?: number; // max
  protein_g?: number;     // min
  carbs_g?: number;       // max
  fiber_g?: number;       // min
  sugar_g?: number;       // max
  fat_g?: number;         // max
  sat_fat_g?: number;     // max
}

export const GOAL_DIRECTION: Record<keyof Goals, 'min' | 'max'> = {
  calories_kcal: 'max',
  protein_g:     'min',
  carbs_g:       'max',
  fiber_g:       'min',
  sugar_g:       'max',
  fat_g:         'max',
  sat_fat_g:     'max',
};

export const NUTRIENT_KEYS = Object.keys(GOAL_DIRECTION) as (keyof Goals)[];

export interface Ingredient {
  name: string;
  calories_kcal?: number;
  protein_g?: number;
  carbs_g?: number;
  fiber_g?: number;
  sugar_g?: number;
  fat_g?: number;
  sat_fat_g?: number;
}

export interface Meal {
  id: string;
  time: string;        // "HH:MM", wall-clock, no timezone
  name: string;
  ingredients: Ingredient[];
}

export type DayLog = Meal[];

export type WeightUnit = 'g' | 'kg' | 'oz' | 'lb';
export type VolumeUnit = 'ml' | 'L' | 'fl_oz' | 'cup' | 'tbsp' | 'tsp';
export type Unit = WeightUnit | VolumeUnit;

export const WEIGHT_UNITS: WeightUnit[] = ['g', 'kg', 'oz', 'lb'];
export const VOLUME_UNITS: VolumeUnit[] = ['ml', 'L', 'fl_oz', 'cup', 'tbsp', 'tsp'];

// Conversion to base units (g for weight, ml for volume)
export const TO_BASE: Record<Unit, number> = {
  g: 1, kg: 1000, oz: 28.3495, lb: 453.592,
  ml: 1, L: 1000, fl_oz: 29.5735, cup: 236.588, tbsp: 14.7868, tsp: 4.92892,
};

export interface FoodEntry {
  per_amount: number;
  per_unit: Unit;
  calories_kcal?: number;
  protein_g?: number;
  carbs_g?: number;
  fiber_g?: number;
  sugar_g?: number;
  fat_g?: number;
  sat_fat_g?: number;
}

export type FoodLibrary = Record<string, FoodEntry>;

export type VecItemType = 'meal' | 'ingredient' | 'food';

export interface VecMeta {
  type: 'meal';
  mealId: string;
  date: string;
}

export interface VecIngredientMeta {
  type: 'ingredient';
  mealId: string;
  index: number;
  date: string;
}

export interface VecFoodMeta {
  type: 'food';
  name: string;
}

export type VecMetadata = VecMeta | VecIngredientMeta | VecFoodMeta;
