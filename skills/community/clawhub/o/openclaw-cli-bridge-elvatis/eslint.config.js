import eslint from "@eslint/js";
import tseslint from "typescript-eslint";

export default tseslint.config(
  eslint.configs.recommended,
  ...tseslint.configs.recommended,
  {
    rules: {
      // Relaxed — this is a plugin, not a library; pragmatism over purity
      "@typescript-eslint/no-explicit-any": "warn",
      "@typescript-eslint/no-unused-vars": ["warn", { argsIgnorePattern: "^_", varsIgnorePattern: "^_" }],
      "@typescript-eslint/no-require-imports": "off", // pre-existing dynamic require in index.ts
      "no-console": "off",
      "prefer-const": "warn", // pre-existing let-without-reassign patterns
      "no-var": "error",
      eqeqeq: ["error", "always"],
      // Pre-existing patterns — suppress until dedicated cleanup
      "no-useless-assignment": "off",
      "no-misleading-character-class": "off",
      "preserve-caught-error": "off",
    },
  },
  {
    ignores: ["dist/", "node_modules/", "test/"],
  },
);
