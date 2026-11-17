module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'node',
  roots: ['<rootDir>/test', '<rootDir>/skills/ops-maintenance/test'],
  testMatch: ['**/*.test.ts'],
  moduleFileExtensions: ['ts', 'tsx', 'js', 'jsx', 'json', 'node'],
  moduleNameMapper: {
    '^@src/(.*)$': '<rootDir>/skills/ops-maintenance/src/$1',
    '^(\\.{1,2}/.*)\\.js$': '$1',
  },
  transform: {
    '^.+\\.tsx?$': ['ts-jest', {
      tsconfig: {
        esModuleInterop: true,
        allowSyntheticDefaultImports: true,
        module: 'ESNext',
        moduleResolution: 'node',
        target: 'ES2020',
        isolatedModules: true,
        skipLibCheck: true,
      }
    }]
  },
  collectCoverageFrom: [
    'skills/ops-maintenance/src/**/*.ts',
    '!skills/ops-maintenance/src/**/*.test.ts',
    '!skills/ops-maintenance/src/index.ts',
    '!skills/ops-maintenance/src/cli.ts',
  ],
  coverageThreshold: {
    global: {
      branches: 50,
      functions: 50,
      lines: 55,
      statements: 55
    }
  },
  setupFilesAfterEnv: ['<rootDir>/test/setup.ts'],
  testTimeout: 15000,
  verbose: true,
}