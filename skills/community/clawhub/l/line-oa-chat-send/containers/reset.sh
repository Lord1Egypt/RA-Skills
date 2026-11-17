#!/usr/bin/env bash
# Remove everything the test environment leaves behind.
#
# Containers are started with --rm, so they clean themselves up. Profile volumes
# are deliberately persistent -- a persistent profile is what the real system
# has -- so removing them is an explicit action.
#
#   containers/reset.sh            drop profile volumes
#   containers/reset.sh --images   also drop the built images
set -euo pipefail

image="${LINE_OA_TEST_IMAGE:-line-oa-test}"
drop_images=0
[[ "${1:-}" == "--images" ]] && drop_images=1

printf 'Stopping any running test containers...\n'
running="$(docker ps -q --filter "ancestor=${image}:full" \
  --filter "ancestor=${image}:no-runtime" \
  --filter "ancestor=${image}:no-handoff-deps" \
  --filter "ancestor=${image}:unauth-profile" 2>/dev/null || true)"
if [[ -n "$running" ]]; then
  # shellcheck disable=SC2086
  docker rm -f $running >/dev/null
  printf '  removed %s container(s)\n' "$(wc -w <<<"$running" | tr -d ' ')"
else
  printf '  none running\n'
fi

printf 'Removing profile volumes...\n'
for variant in full no-runtime no-handoff-deps unauth-profile; do
  if docker volume rm "line-oa-profile-${variant}" >/dev/null 2>&1; then
    printf '  removed line-oa-profile-%s\n' "$variant"
  fi
done

if (( drop_images )); then
  printf 'Removing images...\n'
  for variant in full no-runtime no-handoff-deps unauth-profile; do
    docker rmi "${image}:${variant}" >/dev/null 2>&1 && printf '  removed %s:%s\n' "$image" "$variant"
  done
fi

printf '\nRemaining:\n'
printf '  containers: %s\n' "$(docker ps -aq --filter "ancestor=${image}:full" | wc -l | tr -d ' ')"
printf '  volumes:    %s\n' "$(docker volume ls -q --filter name=line-oa-profile | wc -l | tr -d ' ')"
