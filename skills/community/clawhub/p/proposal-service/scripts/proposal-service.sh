#!/bin/sh
set -eu

DB_CONTAINER="supabase-db"
DB_USER="postgres"
DB_NAME="postgres"
AGENT_ID="c61b873f-354c-431f-9dd7-f627120d576c"

usage() {
  echo "Usage:"
  echo "  proposal-service.sh check-stale-duplicate"
  echo "  proposal-service.sh create-stale-proposal"
  exit 1
}

cmd="${1:-}"
[ -n "$cmd" ] || usage

case "$cmd" in
  check-stale-duplicate)
    docker exec -i "$DB_CONTAINER" psql -U "$DB_USER" -d "$DB_NAME" -At -F $'\t' <<'SQL'
WITH trigger_row AS (
  SELECT *
  FROM public.openclaw_trigger_rules
  WHERE name = 'stale_missions_alert'
    AND enabled = true
  LIMIT 1
),
ctx AS (
  SELECT
    COUNT(*)::int AS stale_count,
    COALESCE(string_agg(title, ' | ' ORDER BY created_at), '') AS titles
  FROM public.openclaw_missions
  WHERE status = 'running'
    AND started_at IS NOT NULL
    AND started_at < now() - make_interval(
      hours => COALESCE((SELECT (conditions->>'threshold_hours')::int FROM trigger_row), 24)
    )
)
SELECT EXISTS (
  SELECT 1
  FROM public.openclaw_proposals p
  CROSS JOIN ctx
  WHERE p.title = 'Heartbeat: misiones estancadas detectadas'
    AND p.description = 'Se detectaron ' || ctx.stale_count || ' misión(es) running con antigüedad superior al umbral. Misiones: ' || ctx.titles
    AND p.status = 'pending'
    AND p.source = 'trigger'
);
SQL
    ;;
  create-stale-proposal)
    docker exec -i "$DB_CONTAINER" psql -U "$DB_USER" -d "$DB_NAME" <<SQL
DO \$\$
DECLARE
  v_stale_count integer := 0;
  v_titles text := '';
BEGIN
  WITH trigger_row AS (
    SELECT *
    FROM public.openclaw_trigger_rules
    WHERE name = 'stale_missions_alert'
      AND enabled = true
    LIMIT 1
  ),
  ctx AS (
    SELECT
      COUNT(*)::int AS stale_count,
      COALESCE(string_agg(title, ' | ' ORDER BY created_at), '') AS titles
    FROM public.openclaw_missions
    WHERE status = 'running'
      AND started_at IS NOT NULL
      AND started_at < now() - make_interval(
        hours => COALESCE((SELECT (conditions->>'threshold_hours')::int FROM trigger_row), 24)
      )
  )
  SELECT stale_count, titles
  INTO v_stale_count, v_titles
  FROM ctx;

  IF v_stale_count = 0 THEN
    RAISE EXCEPTION 'No hay misiones stale. No se crea propuesta.';
  END IF;

  IF EXISTS (
    SELECT 1
    FROM public.openclaw_proposals
    WHERE title = 'Heartbeat: misiones estancadas detectadas'
      AND description = 'Se detectaron ' || v_stale_count || ' misión(es) running con antigüedad superior al umbral. Misiones: ' || v_titles
      AND status = 'pending'
      AND source = 'trigger'
  ) THEN
    RAISE EXCEPTION 'Ya existe una propuesta pending equivalente.';
  END IF;

  INSERT INTO public.openclaw_proposals (
    agent_id,
    title,
    description,
    status,
    proposed_steps,
    source
  ) VALUES (
    '$AGENT_ID'::uuid,
    'Heartbeat: misiones estancadas detectadas',
    'Se detectaron ' || v_stale_count || ' misión(es) running con antigüedad superior al umbral. Misiones: ' || v_titles,
    'pending',
    '[
      {"kind":"analyze","title":"Revisar misiones estancadas detectadas por heartbeat"},
      {"kind":"draft","title":"Preparar propuesta de acción para desbloquearlas"}
    ]'::jsonb,
    'trigger'
  );

  RAISE NOTICE 'Propuesta stale creada correctamente.';
END \$\$;
SQL
    ;;
  *)
    usage
    ;;
esac
