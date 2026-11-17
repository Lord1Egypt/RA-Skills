# Testing — Tables, Parallelism, Fakes, Fuzzing, Benchmarks

Go's testing package is deliberately small: no assertions, no mocking framework, no lifecycle hooks. The compensation is that tests are ordinary Go code, and everything hard about them is a design problem in the code under test.

Sections: Table Tests · Parallelism and Isolation · Fakes Over Mocks · Golden Files · Fuzzing · Benchmarks · Running The Suite · Test Layout and Leaks

## Table Tests

```go
func TestParse(t *testing.T) {
    tests := map[string]struct {
        in      string
        want    Value
        wantErr error
    }{
        "empty input":   {in: "", wantErr: ErrEmpty},
        "leading space": {in: " 1", want: Value{1}},
    }
    for name, tc := range tests {
        t.Run(name, func(t *testing.T) {
            t.Parallel()
            got, err := Parse(tc.in)
            if !errors.Is(err, tc.wantErr) {
                t.Fatalf("err = %v, want %v", err, tc.wantErr)
            }
            if diff := cmp.Diff(tc.want, got); diff != "" {
                t.Errorf("mismatch (-want +got):\n%s", diff)
            }
        })
    }
}
```

- A `map` for cases gives randomized order for free, which catches inter-case dependence. A slice is right when order matters or cases build on each other.
- `t.Run(name, ...)` makes each case addressable with `-run 'TestParse/empty_input'` (spaces become underscores) and keeps failures separate.
- `t.Fatalf` stops this subtest; `t.Errorf` records and continues. Use Fatal when later assertions would panic on the bad value, Error when several independent checks can all report.
- Failure messages state `got` and `want` in that order, with the input. A message that says only "failed" costs a debugging session per occurrence.
- Compare with `cmp.Diff` (google/go-cmp) rather than `reflect.DeepEqual`: it prints a readable diff, and it fails loudly on unexported fields instead of silently comparing them (`structs.md`).

## Parallelism and Isolation

- `t.Parallel()` pauses the subtest until its parent returns, then runs it alongside its siblings, bounded by `-parallel` (default `GOMAXPROCS`).
- Packages always run in parallel with each other. Two packages writing the same file or binding the same port flake in CI and pass locally — use `t.TempDir()` and port `:0`.
- With `go >=1.22` the loop variable is per-iteration, so the `tc := tc` line older code carries is unnecessary. Below that floor it is mandatory, or every parallel subtest tests the last case (`versions.md`).
- `t.Setenv` **panics** if the test or any parent called `t.Parallel()` — the environment is process-wide. Inject configuration instead of setting env vars, or keep that test serial.
- `t.Cleanup(fn)` runs in LIFO order after the test (and after its parallel subtests finish), which is what `defer` cannot do from a helper.
- `t.TempDir()` gives a per-test directory removed automatically; it also fails the test if removal fails, which surfaces leaked open handles on Windows.
- Mark helpers with `t.Helper()` so failures report the caller's line, not the helper's.

## Fakes Over Mocks

- Define the interface in the **consuming** package, small, then implement it with a struct of function fields (`interfaces.md`):

```go
type fakeStore struct{ getFn func(ctx context.Context, id string) (*User, error) }
func (f fakeStore) Get(ctx context.Context, id string) (*User, error) { return f.getFn(ctx, id) }
```

- This needs no code generation, no framework, and no `test_style` decision. Generated mocks (mockgen, mockery) earn their keep for wide interfaces you do not own — with `test_style: testify` the assertion and mock style follows the library instead.
- Assert on **behavior and output**, not on call counts. A test that fails when you add a cache is testing the implementation.
- For HTTP dependencies, `httptest.NewServer` returning recorded payloads beats mocking the client — it exercises the real serialization path (`http.md`).
- For time, inject a clock function; do not sleep (`time.md`).

## Golden Files

- Store expected output under `testdata/` (the toolchain ignores that directory) and regenerate with a flag:

```go
var update = flag.Bool("update", false, "rewrite golden files")
```

- `go test ./... -update` then `git diff` makes the change reviewable — that review is the whole value of the pattern, so a golden test whose diff nobody reads is worse than no test.
- Normalize timestamps, IDs, and map ordering before comparing, or the golden file churns on every run (`collections.md`).

## Fuzzing

```go
func FuzzParse(f *testing.F) {
    f.Add("1,2")                       // seed corpus
    f.Fuzz(func(t *testing.T, s string) {
        v, err := Parse(s)
        if err != nil { return }       // rejecting input is a valid outcome
        if out := v.String(); out != s { /* only assert real invariants */ }
    })
}
```

- `go test -fuzz=FuzzParse` runs until a failure or Ctrl-C; without `-fuzz` the seed corpus runs as a normal test in every CI run.
- Failing inputs are written to `testdata/fuzz/<FuzzName>/` — **commit them**. They become permanent regression cases that run in the normal suite.
- Best targets: parsers, decoders, anything taking bytes from the network, and round-trip properties (`Unmarshal(Marshal(x)) == x`).
- Assert invariants (no panic, round-trip identity, output within bounds), not exact values — fuzzing generates inputs you did not imagine, and an over-specific assertion just produces noise.

## Benchmarks

```go
func BenchmarkEncode(b *testing.B) {
    payload := makePayload()
    b.ReportAllocs()
    b.ResetTimer()                     // exclude setup
    for b.Loop() {                     // go >=1.24; keeps the call from being optimized away
        sink = Encode(payload)
    }
}
var sink []byte                        // package-level, so the result escapes
```

- On `go <1.24` the form is `for i := 0; i < b.N; i++`, and the compiler can delete a call whose result is unused. Assigning to a package-level sink is the classic defense; `b.Loop` removes the need (`versions.md`).
- One run is not a measurement. `go test -bench=X -count=10 -benchmem` and compare with `benchstat`, which reports the delta with a confidence interval — a single before/after pair on a laptop is noise (`performance.md`).
- `b.ResetTimer()` after setup, `b.StopTimer()`/`StartTimer()` around per-iteration setup you cannot hoist.
- `-benchmem` prints B/op and allocs/op. Allocations per operation are the most actionable number in a Go benchmark and the most stable across machines.
- `b.RunParallel` measures contention, which is a different question from single-threaded throughput. Both matter for shared structures (`concurrency.md`).

## Running The Suite

| Command | Purpose |
|---|---|
| `go test ./...` | Everything; results are cached per package |
| `go test -count=1 ./...` | Bypass the cache — the idiomatic "actually re-run it" |
| `go test -race ./...` | Data race detection; the CI default (`debugging.md`) |
| `go test -run 'TestX/case' ./pkg` | One case, by regexp over the subtest path |
| `go test -timeout 30s ./...` | Default is 10 minutes, then a panic with all goroutine stacks |
| `go test -shuffle=on ./...` | Randomize test order; exposes hidden inter-test state |
| `go test -cover -coverprofile=c.out` then `go tool cover -html=c.out` | Coverage, read as a map of untested branches |

- The `-timeout` panic dumps every goroutine stack — that dump is the fastest diagnosis available for a hung test (`debugging.md`).
- `go vet` runs a subset of analyzers automatically during `go test`; a vet failure blocks the run, which is intended.
- Coverage is a *finder of gaps*, not a target. A percentage goal produces tests written for the number.

## Test Layout and Leaks

- `package foo` tests see unexported identifiers; `package foo_test` in the same directory sees only the public API and is the honest test of the package contract. Both are allowed side by side.
- `TestMain(m *testing.M)` for package-level setup; it must call `os.Exit(m.Run())`, and that exit skips defers, so cleanup goes before the call.
- Goroutine leak detection: record `runtime.NumGoroutine()` in `TestMain` before `m.Run()` and fail if the count has grown after, or use `go.uber.org/goleak`. This is how leaks get caught in CI instead of in production (`concurrency.md`).
- Integration tests behind `testing.Short()`: `if testing.Short() { t.Skip("needs a database") }`, then `go test -short` in the fast loop.
- Build-tagged integration files (`//go:build integration`) keep slow suites out of the default run entirely (`build.md`).

## Back To SKILL.md

`change_workflow` in Configuration decides whether the failing test is written before or after the fix — never whether it was seen failing. Race detector cost: `debugging.md`. Benchmark interpretation: `performance.md`.
