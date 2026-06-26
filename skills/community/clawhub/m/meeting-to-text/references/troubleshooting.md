# Troubleshooting

## Validation Errors

Typical cases:
- input file does not exist
- extension is not in the supported audio/video list
- output parent directory cannot be created

These return exit code `1`.

## Media Errors

Typical cases:
- FFmpeg executable is missing
- FFmpeg cannot decode the input media
- normalized WAV was not created

These return exit code `2`.

## Diarization Errors

Typical cases:
- VAD returned nothing usable
- speaker embedding extraction failed
- diarization normalization dropped every segment

These return exit code `3`.

If this happens, do not downgrade to a plain transcript without speaker labels.

## Transcription Errors

Typical cases:
- every usable segment failed ASR
- every segment produced empty text

These return exit code `4`.

## Output Errors

Typical cases:
- transcript file could not be written to the requested location

These return exit code `5`.

## Warnings That Are Still Acceptable

- `only one speaker detected`

This is expected for single-speaker audio and some simple recordings.

## Noisy Stdout

The runtime can print third-party library notices before the final JSON result.

Ignore everything except the last non-empty stdout line when you need machine-readable status.
