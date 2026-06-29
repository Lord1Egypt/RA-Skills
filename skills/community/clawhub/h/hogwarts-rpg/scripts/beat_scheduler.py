#!/usr/bin/env python3
"""
Beat-Scheduler — SCHNITTSTELLE für die Beat-Reihenfolge. In Version 1 LINEAR.

KERNPRINZIP (Auftrag): Der rote Faden ist eine ZEITACHSE, kein Korridor. Die
Kanon-Beats sind an Schuljahr-Zeitpunkten festgenagelt und treffen zu ihrem
Zeitpunkt ein — egal, wo die Spielerin im Sandkasten gerade ist.

VERSION 1 (bewusst robust, ohne reaktive Verschiebung):
Beats sind linear verkettet (`next_scenes[0]`). Andocken und autonome Spur führen
zum SELBEN nächsten Beat. Diese Funktion kapselt genau diese Entscheidung, damit
die Engine einen klaren Aufrufpunkt hat.

SPÄTERER AUSBAU (hier vorbereitet, NICHT implementiert):
Reaktive Beat-Verschiebung / zeit- oder zustandsbasiertes Auslösen (z. B. ein Beat
wartet, bis die Spielerin genug Sandkasten-Zeit hatte; oder ein verpasster Beat
verschiebt einen späteren). Solche Logik kommt HIER hinein — die Engine muss dafür
nur weiterhin `next_beat()` aufrufen.
"""


def next_beat(scene, save=None, plot=None):
    """Liefert die ID des nächsten Kanon-Beats.

    V1: rein linear — erste Folge-Szene. `save`/`plot` werden noch nicht gebraucht,
    sind aber Teil der Signatur, damit späterer reaktiver Code ohne Schnittstellen-
    Bruch andocken kann.
    """
    next_scenes = (scene or {}).get("next_scenes", [])
    return next_scenes[0] if next_scenes else "END"
