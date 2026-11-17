export default {
inject: ['service', 'tags'],
data() {return {
    name: this.$route.query.service,
    app: {service:'', displayName:'', author:'', type:'', ver:'',intVer:0,
     installs:0, cmt:'', recentUpd:'', baseUrl:''},
    subTitle:'',
    preImgNo:0,
    intro:{descrs:[],images:[]},
    baseUrl:'',
    action: '',
    imgWidth:'90vw',
    localVer:0, //服务端安装的版本
    cdns:[]
}},
created() {
    if(document.documentElement.clientWidth>document.documentElement.clientHeight) {
        this.imgWidth="30vw";
    }
    this.service.cdnList().then(cdns=>{
        this.cdns=cdns;
        this.getLocalVer().then(v=> {
            this.getDetail();
        })
    });
},
methods: {
getDetail() {
    var reqOpts={private:false, method:"GET",
        url:"/api/service/detail?service="+this.name,cloud:true};
    request(reqOpts, "appstore").then(resp=>{
        if(resp.code!=RetCode.OK) {
            this.$refs.errDlg.showErr(resp.code, resp.info);
            return;
        }
        var cdnNum=this.cdns.length;
        var cdnNo=Math.floor(Math.random()*cdnNum);
        this.app = resp.data;
        var s = this.cdns[cdnNo]+this.app.service;
        this.app['icon'] = s+"/favicon.png";
        var v = parseInt(resp.data.ver);
        this.app['intVer'] = v;
        this.app.ver=App.intToVer(v);
        this.baseUrl= s + "/" + this.app.ver;
        if(this.localVer<=0) {
            this.action=this.tags.mkt.install;
        } else if(this.localVer<this.app.intVer) {
            this.action=this.tags.mkt.update;
        }
        var dt=new Date(resp.data.recentUpd);
        this.app['updateAt']=dt.toLocaleDateString();
        return this.service.getExternalRes({url:this.baseUrl + "/introduction.json"});
    }).then((s)=> {
        if(!s) {return}
        var o=JSON.parse(s);
        if(!o || !o.introduce) {
            return;
        }
        var intro = o.introduce;
        if(intro.images && intro.images.length > 0) {
            for(var i in intro.images) {
                var src = intro.images[i].src;
                if(src.startsWith("/")) {
                    intro.images[i].src = this.baseUrl+src;
                } else {
                    intro.images[i].src = this.baseUrl + '/' + src;
                }
            }
            this.subTitle = intro.images[0].info;
        }
        this.intro=intro;
    });
},
scroll(event) {
    if(!this.intro||!this.intro.images) {
        return;
    }
    var n=this.intro.images.length;
    var i=parseInt(event.horizontalPercentage*n);
    if(i<n && this.preImgNo!=i) {
        this.subTitle = this.intro.images[i].info;
        this.preImgNo=i;
    }
},
appAction() {
    if (this.localVer>this.app.intVer) {
        this.update(this.app.service);
    } else if(this.localVer<=0) {
        this.install(this.app.service);
    }
},
update(service) {
  this.$refs.procDlg.show(this.tags.mkt.update,
    this.tags.mkt.cfmUpdate+service+'?', 'download',
    (dlg)=> {
        dlg.setInfo(this.tags.mkt.waitting);
        return this.service.command({cmd:"update", service:service},100000);
    },
    (dlg,resp)=> {
      if(resp.code!=RetCode.OK) {
        dlg.setInfo(formatErr(resp.code, resp.info));
      } else {
        this.localVer = this.app.ver;
        dlg.setInfo(this.tags.mkt.successToInstall);
        this.action='';
      }
    }
  )
},
install(service) {
  this.$refs.procDlg.show(this.tags.mkt.install,
    this.tags.mkt.cfmInstall+service+'?', 'download',
    (dlg)=> {
        dlg.setInfo(this.tags.mkt.waitting);
        return this.service.command({cmd:"install", service:service},100000);
    },
    (dlg,resp)=> {
      if(resp.code!=RetCode.OK) {
        dlg.setInfo(formatErr(resp.code, resp.info));
      } else {
        this.localVer = this.app.ver;
        this.action='';
        dlg.setInfo(this.tags.mkt.successToInstall);
      }
    }
  )
},
getLocalVer() {
    var dta = {cmd:"serviceVer", service:this.name};
    return this.service.command(dta).then(resp=>{
        if(resp.code!=RetCode.OK) {
            this.localVer=0;
        } else {
            this.localVer=resp.data.version;
        }
        return this.localVer;
    });
}
},
template: `
<q-layout view="hHh lpr fFf">
  <q-header class="bg-grey-1 text-primary">
   <q-list class="q-pa-sm" dense>
    <q-item>
     <q-item-section thumbnail>
      <q-btn flat round icon="arrow_back" dense @click="service.go_back" class="text-primary"></q-btn>
     </q-avatar></q-item-section>
     <q-item-section avatar><q-avatar square><img :src="app.icon"></q-avatar></q-item-section>
     <q-item-section>
      <q-item-label class="text-primary">{{app.displayName}}/{{app.service}}</q-item-label>
      <q-item-label caption class="text-black">{{tags.mkt.author}} {{app.author}}</q-item-label>
      <q-item-label caption class="text-black">{{tags.mkt.version}} {{app.ver}}</q-item-label>
      <q-item-label caption class="text-black">{{tags.mkt.updateAt}} {{app.updateAt}}</q-item-label>
     </q-item-section>
    </q-item>
   </q-list>
  </q-header>
  <q-footer bordered class="bg-grey-2" v-show="action!=''">
    <q-toolbar class="row justify-center">
      <q-btn rounded color="primary" :label="action" @click="appAction"></q-btn>
    </q-toolbar>
  </q-footer>

   <q-page-container>
     <q-page class="q-pa-none">
<div class="q-py-xs q-px-md">
 <q-chip outline color="primary" text-color="white" icon="cloud_download">{{app.installs}}</q-chip>
</div>
<q-list class="q-pa-sm">
<q-item>
 <q-item-section>
  <q-item-label v-for="descr in intro.descrs" style="text-indent:2em;">{{descr}}</q-item-label>
  <q-item-label caption>{{subTitle}}</q-item-label>
 </q-item-section>
</q-item>
<q-item>
 <q-item-section>
  <q-scroll-area style="height:60vh;width:100%;" horizontal @scroll="scroll">
  <div class="row no-wrap">
   <div v-for="img in intro.images" class="q-pa-sm">
    <q-img :src="img.src" :style="{width:imgWidth}" @click="subTitle=img.info"></q-img>
   </div>
  </div>
  </q-scroll-area>
 </q-item-section>
</q-item>
</q-list>
    </q-page>
  </q-page-container>
</q-layout>
<component-process-dialog ref="procDlg"></component-process-dialog>
<component-alert-dialog :title="tags.failToCall" :errMsgs="tags.errMsgs" :close="tags.close" ref="errDlg"></component-alert-dialog>
`
}