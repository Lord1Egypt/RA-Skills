import SwiftUI
import UIKit

struct DuoRegionFrames {
    var divisions: [CGRect] = []
    var occlusions: [CGRect] = []
}

struct DuoRegionReader<Content: View>: View {
    @ViewBuilder var content: (GeometryProxy, DuoRegionFrames) -> Content

    var body: some View {
        GeometryReader { proxy in
            if #available(iOS 27.1, *) {
                content(proxy, DuoRegionFrames(
                    divisions: proxy.reservedRegions(kind: .division).map(\.frame),
                    occlusions: proxy.reservedRegions(kind: .occlusion).map(\.frame)
                ))
            } else {
                content(proxy, DuoRegionFrames())
            }
        }
    }
}

@MainActor
func duoRegionFrames(in view: UIView) -> DuoRegionFrames {
    #if targetEnvironment(macCatalyst)
    return DuoRegionFrames()
    #else
    if #available(iOS 27.1, *) {
        return DuoRegionFrames(
            divisions: view.reservedRegions(kind: .division).map(\.frame),
            occlusions: view.reservedRegions(kind: .occlusion).map(\.frame)
        )
    }
    return DuoRegionFrames()
    #endif
}
