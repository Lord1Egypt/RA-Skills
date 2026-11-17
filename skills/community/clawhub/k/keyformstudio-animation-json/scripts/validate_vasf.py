#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Validateur VASF (v1/v2/v3/v4/v5/v6) — Keyform Studio simple exchange format.

Vérifie un JSON d'animation AVANT import par fichier dans l'appli (Export ▸
« Importer un fichier JSON… »). Collecte TOUTES les erreurs et les affiche en
français avec leur chemin, comme l'importeur de l'appli.

Usage :
    python3 validate_vasf.py fichier.json
    python3 validate_vasf.py fichier.json --quiet
    echo '{...}' | python3 validate_vasf.py -

Règles source : vector_anim_studio/docs/vasf-1-format.md
Extensions v2 : theme (palette d'alias), layers[], cycle, defs + ref, et
Groupe 2 : scaleX/scaleY (formes + keyframes), pivot, easing cubic-bezier,
liaison de couche « Forme/Couche » dans bind.
Extensions v3 : couleur animée (color/colors), morph de points
(points/layerPoints), translation d'os (move), IK chaînes ≥ 3 os. VASF-4 :
miroir du contenu (flipH/flipV). VASF-5 : rayons et coins de rectangles.
VASF-6 : groupes d'éléments (groups + groupId par NOM).
"""

import argparse
import json
import re
import sys

SHAPES_TYPES = {"rect", "circle", "line", "path", "triangle", "star",
                "hexagon", "cross", "heart", "arrow"}
EASINGS = {"linear", "easeIn", "easeOut", "easeInOut", "step"}
CUBIC_BEZIER = re.compile(
    r"^cubic-bezier\(\s*"
    r"([0-9.eE+-]+)\s*,\s*([0-9.eE+-]+)\s*,"
    r"\s*([0-9.eE+-]+)\s*,\s*([0-9.eE+-]+)\s*\)$")
HEX_COLOR = re.compile(r"^#(?:[0-9A-Fa-f]{8}|[0-9A-Fa-f]{6})$")
DEF_KEYS = {"type", "color", "filled", "strokeWidth", "width", "height",
            "points", "flipH", "flipV", "cornerRadius", "roundTopLeft",
            "roundTopRight", "roundBottomRight", "roundBottomLeft"}
FLAT_GEOMETRY_KEYS = ("type", "color", "filled", "strokeWidth", "width",
                      "height", "points")

errors = []
warnings = []


# v0.17 — import strict : tout champ hors de ces ensembles est refusé
# (auparavant ignoré en silence : liage perdu, animation immobile).
TOP_KNOWN_KEYS = {"version", "name", "canvas", "theme", "defs",
                  "shapes", "skeleton", "groups"}
GROUP_KNOWN_KEYS = {"name", "color", "visible", "collapsed", "x", "y",
                    "rotation", "scaleX", "scaleY"}
CANVAS_KNOWN_KEYS = {"width", "height", "fps", "background"}
SHAPE_KNOWN_KEYS = {
    "name", "ref", "layers", "type", "color", "filled", "strokeWidth",
    "width", "height", "points", "x", "y", "rotation", "scale", "scaleX",
    "scaleY", "pivot", "opacity", "start", "end", "keyframes", "cycle",
    "bone", "flipH", "flipV", "cornerRadius", "roundTopLeft",
    "roundTopRight", "roundBottomRight", "roundBottomLeft", "groupId",
}
BONE_KNOWN_KEYS = {"name", "parent", "joint", "angle", "length", "z", "ik",
                   "bend", "keyframes", "cycle"}

# Raccourcis « bone » des formes (path, forme, os) — croisés avec les os
# et skeleton.bind dans check_skeleton.
SHAPE_BONE_SHORTCUTS = []


def err(path, msg):
    errors.append("%s : %s" % (path, msg))


def warn(path, msg):
    warnings.append("%s : %s" % (path, msg))


def is_num(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def is_int(v):
    return isinstance(v, int) and not isinstance(v, bool)


def is_pair(v):
    return (isinstance(v, list) and len(v) == 2
            and all(is_num(x) for x in v))


def check_easing(v, path):
    """Easing nommé OU chaîne CSS cubic-bezier(x1, y1, x2, y2) (v2 G2)."""
    if not isinstance(v, str):
        err(path, "doit être une chaîne (nommé ou cubic-bezier(…))")
        return
    if v in EASINGS:
        return
    m = CUBIC_BEZIER.match(v)
    if m is None:
        err(path,
            "« %s » inconnu → linear, easeIn, easeOut, easeInOut, step "
            "ou cubic-bezier(x1, y1, x2, y2)" % v)
        return
    try:
        xs = [float(m.group(1)), float(m.group(3))]
        ys = [float(m.group(2)), float(m.group(4))]
    except ValueError:
        err(path, "cubic-bezier(x1, y1, x2, y2) — 4 nombres attendus")
        return
    for label, x in zip(("x1", "x2"), xs):
        if not 0 <= x <= 1:
            err(path + ".%s" % label,
                "%.3f hors [0, 1] (progression monotone obligatoire)" % x)
    for label, y in zip(("y1", "y2"), ys):
        if not -10 <= y <= 10:
            warn(path + ".%s" % label,
                 "%.3f très au-delà de 0–1 (rebond élastique ?)" % y)


def check_color(v, path, what, aliases=None):
    if isinstance(v, str) and v.startswith("$"):
        alias = v[1:]
        if aliases is None or alias not in aliases:
            err(path, "alias « %s » inconnu (définir « theme.%s »)"
                % (alias, alias))
        return
    if not isinstance(v, str) or not HEX_COLOR.match(v):
        err(path, "%s doit être une chaîne '#RRGGBB', '#AARRGGBB' ou un "
                  "alias « $nom »" % what)


def check_primitive_fields(o, path, aliases, with_pose=False):
    """Champs de primitive communs : forme à plat, couche, définition."""
    if o.get("type") is not None and o.get("type") not in SHAPES_TYPES:
        err(path + ".type",
            "« %s » inconnu → choisir parmi rect, circle, line, path, "
            "triangle, star, hexagon, cross, heart, arrow" % o.get("type"))
    if "color" in o:
        check_color(o["color"], path + ".color", "couleur", aliases)
    if "filled" in o and not isinstance(o["filled"], bool):
        err(path + ".filled", "doit être true (rempli) ou false (contour)")
    nums = ["strokeWidth", "width", "height"]
    if with_pose:
        nums += ["x", "y", "rotation", "scale", "opacity"]
    for f in nums:
        if f in o and not is_num(o[f]):
            err(path + "." + f, "doit être un nombre")
    if "opacity" in o and with_pose and not (0 <= o["opacity"] <= 1):
        err(path + ".opacity", "doit être entre 0 et 1")
    if o.get("type") == "path":
        pts = o.get("points")
        if not isinstance(pts, list) or len(pts) < 2:
            err(path + ".points",
                "type path : liste d'au moins 2 points [x, y]")
        else:
            for j, p in enumerate(pts):
                if not is_pair(p):
                    err(path + ".points[%d]" % j, "doit être une paire [x, y]")
    elif "points" in o:
        warn(path + ".points",
             "présent mais ignoré (points réservés au type path)")


def check_layer(layer, path, aliases, with_pose=True):
    if not isinstance(layer, dict):
        err(path, "doit être un objet")
        return
    if "name" in layer and not isinstance(layer["name"], str):
        err(path + ".name", "doit être une chaîne")
    check_primitive_fields(layer, path, aliases, with_pose=with_pose)
    if "zIndex" in layer:
        warn(path + ".zIndex", "zIndex de forme ignoré dans layers[]")
    # v0.19 : miroir du contenu par couche — booléens obligatoires.
    for f in ("flipH", "flipV"):
        if f in layer and not isinstance(layer[f], bool):
            err(path + "." + f, "doit être un booléen")
    # VASF-5 : rayon et choix des coins ne s'appliquent qu'aux rectangles.
    if "cornerRadius" in layer:
        if not is_num(layer["cornerRadius"]) or layer["cornerRadius"] < 0:
            err(path + ".cornerRadius", "doit être un nombre ≥ 0")
    for f in ("roundTopLeft", "roundTopRight", "roundBottomRight",
              "roundBottomLeft"):
        if f in layer and not isinstance(layer[f], bool):
            err(path + "." + f, "doit être un booléen")
    if layer.get("type") not in (None, "rect") and any(
            f in layer for f in ("cornerRadius", "roundTopLeft", "roundTopRight",
                                 "roundBottomRight", "roundBottomLeft")):
        warn(path, "réglages de coins ignorés : type rect requis")
    # vasf-2 G2 : le pivot est un réglage au niveau FORME — dans layers[]
    # l'appli l'ignore (et la forme tourne autour de son centre).
    if "pivot" in layer:
        err(path + ".pivot",
            "le pivot de rotation se règle au niveau de la FORME (champ "
            "« pivot » de la forme, ex. porte : [-largeur/2, 0]), pas dans "
            "layers[]")
    extra = sorted(
        k for k in layer
        if k not in ("name", "type", "color", "filled", "strokeWidth",
                     "width", "height", "points", "x", "y", "rotation",
                     "scale", "opacity", "flipH", "flipV", "cornerRadius",
                     "roundTopLeft", "roundTopRight", "roundBottomRight",
                     "roundBottomLeft")
    )
    if extra:
        warn(path, "champ(s) %s ignoré(s) dans layers[]" % ", ".join(extra))
    if layer.get("type") in (None, "rect", "circle"):
        if "width" not in layer and "height" not in layer:
            warn(path + ".width/.height",
                 "absents → défaut 110/110 (taille de la primitive)")


def check_cycle(cycle, path, has_keyframes):
    if cycle is None:
        return
    if not isinstance(cycle, dict):
        err(path, 'doit être un objet {"repeat": N}')
        return
    extra = [k for k in cycle if k != "repeat"]
    if extra:
        warn(path, "champ(s) %s ignoré(s) (seul « repeat » est lu)"
            % ", ".join(sorted(extra)))
    rep = cycle.get("repeat")
    if rep is None:
        err(path + ".repeat", "requis (entier ≥ 1)")
    elif not is_int(rep) or rep < 1:
        err(path + ".repeat", "doit être un entier ≥ 1 (trouvé : %r)" % rep)
    elif not has_keyframes:
        warn(path, "cycle sans keyframes → ignoré à l'import")


def check_shape(sk, i, aliases, def_names):
    path = "shapes[%d]" % i
    if not isinstance(sk, dict):
        err(path, "doit être un objet")
        return

    name = sk.get("name")
    if name is None:
        warn(path + ".name", "absent → défaut « Forme »")
        name = "Forme"
    elif not isinstance(name, str):
        err(path + ".name", "doit être une chaîne")

    ref = sk.get("ref")
    if ref is not None:
        if not isinstance(ref, str) or not ref.strip():
            err(path + ".ref",
                "doit être un nom de définition (texte non vide)")
        elif ref not in def_names:
            err(path + ".ref", "définition « %s » inconnue (clés « defs » : %s)"
                % (ref, ", ".join(sorted(def_names)) or "aucune"))

    # v0.17 : raccourci de liage « bone » + champs inconnus refusés.
    if "bone" in sk:
        b = sk["bone"]
        if isinstance(b, str) and b.strip():
            SHAPE_BONE_SHORTCUTS.append((path, name, b.strip()))
        else:
            err(path + ".bone", "doit être un nom d'os (chaîne non vide)")
    extra = sorted(k for k in sk if k not in SHAPE_KNOWN_KEYS)
    if extra:
        err(path, "champ(s) inconnu(s) %s — refusé(s) depuis v0.17 "
                  "(auparavant ignorés en silence)" % ", ".join(extra))

    layers = sk.get("layers")
    if layers is not None:
        if not isinstance(layers, list) or len(layers) < 1:
            err(path + ".layers", "doit être un tableau d'au moins 1 couche")
            layers = []
        for j, layer in enumerate(layers):
            check_layer(layer, "%s.layers[%d]" % (path, j), aliases)
        flat = [k for k in FLAT_GEOMETRY_KEYS if k in sk]
        if flat:
            warn(path, "champ(s) plat(s) %s ignoré(s) : la géométrie vient "
                       "de « layers »" % ", ".join(flat))
    else:
        check_primitive_fields(sk, path, aliases)
        if ref is None and sk.get("type") in (None, "rect", "circle"):
            if "width" not in sk and "height" not in sk:
                warn(path + ".width/.height",
                     "absents → défaut 110/110 (taille de la primitive)")

    if "scale" in sk and is_num(sk["scale"]) and not (0.05 <= sk["scale"] <= 4):
        warn(path + ".scale",
             "%.3f hors plage recommandée 0.05–4" % sk["scale"])

    # vasf-2 G2 : facteurs d'axe de base + pivot de rotation.
    for f in ("scaleX", "scaleY"):
        if f in sk:
            if not is_num(sk[f]):
                err(path + "." + f, "doit être un nombre")
            elif not (0.05 <= sk[f] <= 4):
                warn(path + "." + f,
                     "%.3f hors plage recommandée 0.05–4" % sk[f])
    if "pivot" in sk:
        if not is_pair(sk["pivot"]):
            err(path + ".pivot",
                "doit être une paire [dx, dy] en unités de forme")
        elif any(abs(x) > 500 for x in sk["pivot"]):
            warn(path + ".pivot",
                 "offset %s très grand — pivot attendu près du centre "
                 "(bord d'une forme 110 → ±55)" % sk["pivot"])

    if "opacity" in sk:
        if not is_num(sk["opacity"]) or not (0 <= sk["opacity"] <= 1):
            err(path + ".opacity", "doit être entre 0 et 1")

    # Fenêtre d'affichage ACTIVE : la forme n'est rendue que sur
    # [start, end] ; end par défaut = la fin la plus tardive des autres
    # formes, sinon 4 s ; une keyframe au-delà de end PROLONGE end.
    start = sk.get("start", 0.0)
    end = sk.get("end")
    if not is_num(start) or start < 0:
        err(path + ".start", "doit être un nombre de secondes ≥ 0")
    if end is not None:
        if not is_num(end):
            err(path + ".end", "doit être un nombre de secondes")
        elif is_num(start) and end <= start:
            err(path + ".end",
                "fin > début attendue (%s ≤ %s)" % (end, start))

    kfs = sk.get("keyframes")
    has_kfs = isinstance(kfs, list) and len(kfs) > 0
    if kfs is not None:
        if not isinstance(kfs, list):
            err(path + ".keyframes", "doit être un tableau")
            kfs = []
        # vasf-3 : le contexte détermine le champ couleur/morph autorisé.
        is_multi = sk.get("layers") is not None
        layer_names = [
            l.get("name") for l in (sk.get("layers") or [])
            if isinstance(l, dict) and isinstance(l.get("name"), str)
        ] if is_multi else None
        for j, kf in enumerate(kfs):
            check_shape_kf(kf, "%s.keyframes[%d]" % (path, j),
                           is_multi=is_multi, layer_names=layer_names,
                           aliases=aliases)

    check_cycle(sk.get("cycle"), path + ".cycle", has_kfs)

    # vasf-3 : un nuage de morph qui ne commence pas à t ≈ 0 → la BASE est
    # affichée au début (les nuages sont portés de keyframe en keyframe).
    if has_kfs and isinstance(kfs, list):
        morph_ts = [
            kf.get("t") for kf in kfs
            if isinstance(kf, dict)
            and ("points" in kf or "layerPoints" in kf)
            and is_num(kf.get("t"))
        ]
        if morph_ts and min(morph_ts) > 0.3:
            warn(path + ".keyframes",
                 "le morph démarre à %.2f s — avant cette keyframe la BASE "
                 "est affichée ; ajouter le nuage de départ (copie de la "
                 "base) à t ≈ 0" % min(morph_ts))


def _check_point_cloud(cloud, path):
    """vasf-3 : nuage de points [x, y], au moins 2 points."""
    if not isinstance(cloud, list) or len(cloud) < 2:
        err(path, "doit être une liste d'au moins 2 points [x, y]")
        return
    for i, p in enumerate(cloud):
        if not is_pair(p):
            err("%s[%d]" % (path, i), "doit être une paire [x, y]")


def check_shape_kf(kf, path, is_multi=False, layer_names=None, aliases=None):
    if not isinstance(kf, dict):
        err(path, "doit être un objet")
        return
    t = kf.get("t")
    if t is None:
        err(path + ".t", "requis (secondes, ≥ 0)")
    elif not is_num(t) or t < 0:
        err(path + ".t", "doit être un nombre de secondes ≥ 0")
    if "easing" in kf:
        check_easing(kf["easing"], path + ".easing")
    for f in ("x", "y", "rotation", "scale", "scaleX", "scaleY", "strokeWidth"):
        if f in kf and not is_num(kf[f]):
            err(path + "." + f, "doit être un nombre")
    for f in ("scaleX", "scaleY"):
        if f in kf and is_num(kf[f]) and not (0.05 <= kf[f] <= 4):
            warn(path + "." + f,
                 "%.3f hors plage recommandée 0.05–4" % kf[f])
    if "opacity" in kf:
        if not is_num(kf["opacity"]) or not (0 <= kf["opacity"] <= 1):
            err(path + ".opacity", "doit être entre 0 et 1")

    # vasf-3 : couleur animée (`color` à plat / `colors` par couche).
    if "color" in kf:
        if is_multi:
            err(path + ".color",
                "réservé aux formes à UNE couche — pour une forme en "
                "layers[], utiliser « colors » (nom de couche → hex)")
        else:
            check_color(kf["color"], path + ".color", "couleur", aliases)
    if "colors" in kf:
        if not is_multi:
            err(path + ".colors",
                "réservé aux formes en layers[] — pour une forme à une "
                "couche, utiliser « color »")
        elif not isinstance(kf["colors"], dict):
            err(path + ".colors",
                "doit être un objet {nom de couche → couleur}")
        else:
            for lname, color in kf["colors"].items():
                if layer_names is not None and lname not in layer_names:
                    err(path + ".colors.%s" % lname,
                        "couche inconnue (couches : %s)"
                        % (", ".join(layer_names) or "aucune"))
                else:
                    check_color(color, path + ".colors." + lname,
                                "couleur", aliases)

    # vasf-3 : morph de points (`points` à plat / `layerPoints` par couche).
    if "points" in kf:
        if is_multi:
            err(path + ".points",
                "réservé aux formes à UNE couche — pour une forme en "
                "layers[], utiliser « layerPoints »")
        else:
            _check_point_cloud(kf["points"], path + ".points")
    if "layerPoints" in kf:
        if not is_multi:
            err(path + ".layerPoints",
                "réservé aux formes en layers[] — pour une forme à une "
                "couche, utiliser « points »")
        elif not isinstance(kf["layerPoints"], dict):
            err(path + ".layerPoints",
                "doit être un objet {nom de couche → points}")
        else:
            for lname, cloud in kf["layerPoints"].items():
                if layer_names is not None and lname not in layer_names:
                    err(path + ".layerPoints.%s" % lname,
                        "couche inconnue (couches : %s)"
                        % (", ".join(layer_names) or "aucune"))
                else:
                    _check_point_cloud(cloud,
                                       path + ".layerPoints." + lname)


def _check_bone_keyframe(kf, kpath, by_name, require_bone=True):
    """Vérifie une keyframe d'os (squelette OU embarquée dans l'os, v0.17)."""
    if require_bone and kf.get("bone") not in by_name:
        err(kpath + ".bone",
            "« %s » inconnu (nom d'os requis)" % kf.get("bone"))
    t = kf.get("t")
    if t is None:
        err(kpath + ".t", "requis (secondes, ≥ 0)")
    elif not is_num(t) or t < 0:
        err(kpath + ".t", "doit être un nombre de secondes ≥ 0")
    if "easing" in kf:
        check_easing(kf["easing"], kpath + ".easing")
    for f in ("angle", "stretch", "squash"):
        if f in kf and not is_num(kf[f]):
            err(kpath + "." + f, "doit être un nombre")
    if "opacity" in kf:
        if not is_num(kf["opacity"]) or not (0 <= kf["opacity"] <= 1):
            err(kpath + ".opacity", "doit être entre 0 et 1")
    # vasf-3 : translation d'os `move` [dx, dy] monde.
    if "move" in kf and not is_pair(kf["move"]):
        err(kpath + ".move",
            "doit être une paire [dx, dy] en coordonnées monde")
    if "angle" not in kf and "move" not in kf:
        warn(kpath, "sans `angle` ni `move`, la keyframe ne pose que "
                    "opacité/étirement/écrasement")


def check_bones(bones, sk_path):
    """Retourne (noms dans l'ordre, dict name→index)."""
    names = []
    by_name = {}
    for i, b in enumerate(bones):
        path = "%s.bones[%d]" % (sk_path, i)
        if not isinstance(b, dict):
            err(path, "doit être un objet")
            continue
        n = b.get("name")
        if not n:
            err(path + ".name", "requis (nom unique de l'os)")
            n = "__sans_nom_%d" % i
        elif n in by_name:
            err(path + ".name", "« %s » déjà utilisé (noms d'os uniques)" % n)
        else:
            by_name[n] = i
        names.append(n)

        joint = b.get("joint")
        if joint is None:
            err(path + ".joint", "requis [x, y] en coordonnées canvas (repos)")
        elif not is_pair(joint):
            err(path + ".joint", "doit être une paire [x, y]")

        for f in ("angle", "length", "z"):
            if f in b and not is_num(b[f]):
                err(path + "." + f, "doit être un nombre")
        if "length" in b and b["length"] <= 0:
            err(path + ".length", "doit être > 0")
        if "z" in b and is_num(b["z"]) and not (-10 <= b["z"] <= 10):
            warn(path + ".z", "%.1f hors plage -10…+10" % b["z"])
        if "ik" in b and not isinstance(b["ik"], bool):
            err(path + ".ik", "doit être true ou false")
        if "bend" in b and b["bend"] not in (1, -1):
            err(path + ".bend", "doit être +1 ou -1 (côté du coude IK)")

        parent = b.get("parent")
        if parent is not None and parent not in names:
            err(path + ".parent",
                "« %s » inconnu — les parents doivent être DÉCLARÉS AVANT "
                "leurs enfants (réordonner la liste bones)" % parent)

        # v0.17 : keyframes/cycle EMBARQUÉS dans l'os (même sémantique que
        # skeleton.keyframes, l'os est implicite) + champs inconnus refusés.
        emb_kfs = b.get("keyframes")
        has_emb = isinstance(emb_kfs, list) and len(emb_kfs) > 0
        if emb_kfs is not None:
            if not isinstance(emb_kfs, list):
                err(path + ".keyframes", "doit être un tableau")
            else:
                for j, kf in enumerate(emb_kfs):
                    kpath = "%s.keyframes[%d]" % (path, j)
                    if not isinstance(kf, dict):
                        err(kpath, "doit être un objet")
                        continue
                    if "bone" in kf:
                        warn(kpath + ".bone",
                             "inutile dans une keyframe embarquée dans l'os "
                             "(l'os est implicite)")
                    _check_bone_keyframe(kf, kpath, by_name,
                                         require_bone=False)
        check_cycle(b.get("cycle"), path + ".cycle", has_emb)

        extra = sorted(k for k in b if k not in BONE_KNOWN_KEYS)
        if extra:
            err(path, "champ(s) inconnu(s) %s — refusé(s) depuis v0.17 "
                      "(auparavant ignorés en silence)" % ", ".join(extra))
    return names, by_name


def check_groups(raw, shapes):
    """Groupes d'éléments (v6) : noms uniques, champs connus, et chaque
    `groupId` de forme doit désigner un groupe déclaré."""
    declared = set()
    if raw is not None:
        if not isinstance(raw, list):
            err("groups", "doit être un tableau de groupes")
            raw = []
        for i, g in enumerate(raw):
            path = "groups[%d]" % i
            if not isinstance(g, dict):
                err(path, "doit être un objet")
                continue
            name = g.get("name")
            if not isinstance(name, str) or not name.strip():
                err(path + ".name", "nom de groupe non vide requis")
            elif name in declared:
                err(path + ".name",
                    "groupe « %s » déjà défini (noms uniques)" % name)
            else:
                declared.add(name)
            extra = sorted(k for k in g if k not in GROUP_KNOWN_KEYS)
            if extra:
                err(path, "champ(s) inconnu(s) %s — refusé(s) depuis v0.17"
                    % ", ".join(extra))
            if "color" in g:
                check_color(g["color"], path + ".color", "couleur", {})
            for f in ("visible", "collapsed"):
                if f in g and not isinstance(g[f], bool):
                    err(path + "." + f, "doit être un booléen")
            for f in ("x", "y", "rotation", "scaleX", "scaleY"):
                if f in g and not is_num(g[f]):
                    err(path + "." + f, "doit être un nombre")
            for f in ("scaleX", "scaleY"):
                if f in g and is_num(g[f]) and not (0.05 <= g[f] <= 4):
                    warn(path + "." + f,
                         "%.3f hors plage recommandée 0.05–4" % g[f])

    # Chaque forme rattachée doit viser un groupe déclaré.
    for i, s in enumerate(shapes):
        if not isinstance(s, dict):
            continue
        gid = s.get("groupId")
        if gid is None:
            continue
        if not isinstance(gid, str) or not gid.strip():
            err("shapes[%d].groupId" % i,
                "nom de groupe attendu (chaîne non vide)")
        elif gid not in declared:
            err("shapes[%d].groupId" % i,
                "groupe « %s » inconnu (déclarer une entrée « groups » de "
                "ce nom)" % gid)


def check_skeleton(skel, canvas, shape_names, aliases, shape_layers=None):
    path = "skeleton"
    if not isinstance(skel, dict):
        err(path, "doit être un objet")
        return

    bones = skel.get("bones")
    if not isinstance(bones, list) or len(bones) < 1:
        err(path + ".bones", "requis : tableau d'au moins 1 os")
        return

    names, by_name = check_bones(bones, path)

    # IK (v0.15 : chaînes) : la racine IK doit avoir AU MOINS un enfant ;
    # la chaîne suit les os à enfant UNIQUE — un os à plusieurs enfants
    # arrête la chaîne (l'effecteur = extrémité du dernier os).
    for i, b in enumerate(bones):
        if isinstance(b, dict) and b.get("ik"):
            children = [j for j, other in enumerate(bones)
                        if isinstance(other, dict)
                        and other.get("parent") == b.get("name")]
            if len(children) == 0:
                err(path + ".bones[%d]" % i,
                    "ik: true exige au moins un enfant — os « %s » en a 0 "
                    "(chaîne d'un seul os, sans effecteur)" % b.get("name"))
            elif len(children) > 1:
                warn(path + ".bones[%d]" % i,
                     "os « %s » a %d enfants : la chaîne IK s'arrête à lui "
                     "(l'IK suit les os à enfant unique)"
                     % (b.get("name"), len(children)))

    bind = skel.get("bind")
    if bind is not None:
        if not isinstance(bind, dict):
            err(path + ".bind", "doit être un objet {nom forme → nom os}")
        else:
            if shape_layers is None:
                shape_layers = {}
            for s_name, b_name in bind.items():
                # vasf-2 G2 : clé « Forme/Couche » = liaison d'une couche.
                slash = s_name.find("/")
                if slash < 0:
                    layer_name = None
                    shape_key = s_name
                else:
                    shape_key = s_name[:slash]
                    layer_name = s_name[slash + 1:]
                if shape_key not in shape_names:
                    err(path + ".bind[\"%s\"]" % s_name,
                        "aucune forme ne porte ce nom (liaison par NOMS)")
                elif layer_name is not None:
                    layers = shape_layers.get(shape_key, [])
                    if layer_name not in layers:
                        err(path + ".bind[\"%s\"]" % s_name,
                            "couche « %s » inconnue sur la forme « %s » "
                            "(couches : %s)"
                            % (layer_name, shape_key,
                               ", ".join(layers) or "aucune"))
                if b_name not in by_name:
                    err(path + ".bind[\"%s\"]" % s_name,
                        "aucun os ne s'appelle « %s »" % b_name)

    # v0.17 : raccourcis « bone » des formes — l'os doit exister et ne pas
    # entrer en conflit avec un skeleton.bind existant.
    bound = skel.get("bind") if isinstance(skel.get("bind"), dict) else {}
    for spath, s_name, b_name in SHAPE_BONE_SHORTCUTS:
        if b_name not in by_name:
            err(spath + ".bone", "aucun os ne s'appelle « %s »" % b_name)
        elif s_name in shape_names and bound.get(s_name) not in (None, b_name):
            err(spath + ".bone",
                "conflit : la forme « %s » est aussi liée à « %s » par "
                "skeleton.bind" % (s_name, bound.get(s_name)))

    kfs = skel.get("keyframes")
    has_kfs = isinstance(kfs, list) and len(kfs) > 0

    check_cycle(skel.get("cycle"), path + ".cycle", has_kfs)

    if kfs is not None:
        if not isinstance(kfs, list):
            err(path + ".keyframes", "doit être un tableau")
            return
        for j, kf in enumerate(kfs):
            kpath = "%s.keyframes[%d]" % (path, j)
            if not isinstance(kf, dict):
                err(kpath, "doit être un objet")
                continue
            _check_bone_keyframe(kf, kpath, by_name)


def validate(doc):
    del SHAPE_BONE_SHORTCUTS[:]
    if not isinstance(doc, dict):
        err("$", "le fichier doit contenir UN SEUL objet JSON d'animation")
        return
    extra = sorted(k for k in doc if k not in TOP_KNOWN_KEYS
                   and not k.startswith("example") and k != "_readme")
    if extra:
        err("$", "champ(s) racine inconnu(s) %s — refusé(s) depuis v0.17"
            % ", ".join(extra))

    wrapper_keys = [k for k in doc if k.startswith("example")]
    if wrapper_keys or "_readme" in doc:
        err("$", "ce fichier est le recueil d'exemples (clés %s…) — l'appli "
                 "importe UN SEUL objet : extraire l'objet d'exemple "
                 "(ou valider avec --pick CLE)"
            % ", ".join(wrapper_keys))
        return

    version = doc.get("version")
    if version not in (1, 2, 3, 4, 5, 6):
        err("version", "requis et doit être 1, 2, 3, 4, 5 ou 6 (trouvé : %r)"
            % version)

    # Palette « theme » (v2) : alias littéraux uniquement.
    aliases = set()
    theme = doc.get("theme")
    if theme is not None:
        if not isinstance(theme, dict):
            err("theme", "doit être un objet {alias → couleur}")
        else:
            for alias, color in theme.items():
                if not (isinstance(color, str) and HEX_COLOR.match(color)):
                    err("theme.%s" % alias,
                        "doit être une couleur littérale '#RRGGBB' "
                        "(un alias « $… » ne peut pas en référencer un autre)")
                else:
                    aliases.add(alias)

    # Définitions réutilisables (v2).
    def_names = set()
    used_refs = set()
    defs = doc.get("defs")
    if defs is not None:
        if not isinstance(defs, dict):
            err("defs", "doit être un objet {nom → définition}")
        else:
            for name, d in defs.items():
                dpath = "defs.%s" % name
                if not isinstance(d, dict):
                    err(dpath, "doit être un objet (géométrie de primitive)")
                    continue
                def_names.add(name)
                # Géométrie seule : pas de pose dans une définition.
                check_layer(d, dpath, aliases, with_pose=False)
                extra = sorted(k for k in d if k not in DEF_KEYS)
                if extra:
                    warn(dpath, "champ(s) %s ignoré(s) dans une définition "
                                "(géométrie seule)" % ", ".join(extra))

    canvas = doc.get("canvas", {})
    if not isinstance(canvas, dict):
        err("canvas", "doit être un objet")
        canvas = {}
    for f, lo, hi in (("width", 16, 4096), ("height", 16, 4096)):
        v = canvas.get(f)
        if v is None:
            warn("canvas." + f,
                 "absent → défaut %d" % (720 if f == "width" else 1280))
        elif not is_num(v) or not (lo <= v <= hi):
            err("canvas." + f, "doit être un nombre entre %d et %d" % (lo, hi))
    fps = canvas.get("fps")
    if fps is None:
        warn("canvas.fps", "absent → défaut 25")
    elif not is_num(fps) or not (5 <= fps <= 60):
        err("canvas.fps", "doit être un entier entre 5 et 60")
    if "background" in canvas:
        check_color(canvas["background"], "canvas.background", "fond", aliases)
    extra = sorted(k for k in canvas if k not in CANVAS_KNOWN_KEYS)
    if extra:
        err("canvas", "champ(s) inconnu(s) %s — refusé(s) depuis v0.17"
            % ", ".join(extra))

    shapes = doc.get("shapes")
    if not isinstance(shapes, list) or len(shapes) < 1:
        err("shapes", "requis : tableau d'au moins 1 forme")
        shapes = []
    shape_names = []
    shape_layers = {}
    seen = set()
    for i, s in enumerate(shapes):
        if isinstance(s, dict) and isinstance(s.get("name"), str):
            if s["name"] in seen:
                warn("shapes[%d].name" % i,
                     "« %s » dupliqué → renommé auto « %s 2 » à l'import"
                     % (s["name"], s["name"]))
            seen.add(s["name"])
            shape_names.append(s["name"])
            layers = s.get("layers")
            if isinstance(layers, list):
                shape_layers[s["name"]] = [
                    l.get("name") for l in layers
                    if isinstance(l, dict) and isinstance(l.get("name"), str)
                ]
        if isinstance(s, dict) and isinstance(s.get("ref"), str):
            used_refs.add(s["ref"])
        check_shape(s, i, aliases, def_names)

    for name in sorted(def_names - used_refs):
        warn("defs.%s" % name,
             "définition jamais utilisée (aucune forme ne fait « ref » dessus)")

    check_groups(doc.get("groups"), shapes)

    if "skeleton" in doc and doc["skeleton"] is not None:
        check_skeleton(doc["skeleton"], canvas, shape_names, aliases,
                       shape_layers=shape_layers)


def collection_keys(doc):
    """Clés d'exemples d'un recueil (dict dont les valeurs sont des objets
    d'animation), ou None si le document n'est pas un recueil."""
    if not isinstance(doc, dict):
        return None
    keys = [k for k in doc if k.startswith("example")
            and isinstance(doc[k], dict) and isinstance(doc[k].get("shapes"),
                                                        list)]
    return keys or None


def validate_collection(doc, keys, quiet):
    """Valide chaque objet d'un recueil ; renvoie le nombre d'erreurs."""
    total = 0
    for key in keys:
        del errors[:]
        del warnings[:]
        validate(doc[key])
        if not quiet:
            for w in warnings:
                print("⚠ %s : %s" % (key, w))
            for e in errors:
                print("✘ %s : %s" % (key, e))
        total += len(errors)
        if not errors:
            ver = doc[key].get("version")
            print("✔ %s : VASF-%s valide" % (key, ver))
    return total


def main():
    ap = argparse.ArgumentParser(description="Validateur VASF (v1/v2/v3/v4/v5/v6)")
    ap.add_argument("file", help="fichier .json, ou - pour stdin")
    ap.add_argument("--quiet", action="store_true",
                    help="afficher uniquement le verdict")
    ap.add_argument("--pick", default=None,
                    help="clé d'un objet dans un recueil d'exemples")
    args = ap.parse_args()

    try:
        raw = sys.stdin.read() if args.file == "-" else open(
            args.file, encoding="utf-8").read()
        doc = json.loads(raw)
    except Exception as e:  # noqa: BLE001
        print("✘ JSON illisible : %s" % e)
        sys.exit(2)

    keys = collection_keys(doc)
    if keys is not None:
        if args.pick is not None:
            if args.pick not in keys:
                print("✘ --pick %s : clés disponibles : %s"
                      % (args.pick, ", ".join(keys)))
                sys.exit(2)
            keys = [args.pick]
        total = validate_collection(doc, keys, args.quiet)
        if total:
            print("\n✘ %d erreur(s) dans le recueil — corriger avant import"
                  % total)
            sys.exit(1)
        print("\n✔ recueil valide : %d objet(s) importables un par un"
              % len(keys))
        sys.exit(0)

    validate(doc)

    if not args.quiet:
        for w in warnings:
            print("⚠ %s" % w)
        for e in errors:
            print("✘ %s" % e)
    if errors:
        print("\n✘ %d erreur(s) — corriger avant import" % len(errors))
        sys.exit(1)
    ver = doc.get("version") if isinstance(doc, dict) else None
    label = "VASF-%s" % ver if ver in (1, 2, 3, 4, 5) else "VASF"
    print("\n✔ %s valide — prêt à importer (Export ▸ « Importer un fichier "
          "JSON… »)" % label
          + (" (%d remarque(s))" % len(warnings) if warnings else ""))
    sys.exit(0)


if __name__ == "__main__":
    main()
