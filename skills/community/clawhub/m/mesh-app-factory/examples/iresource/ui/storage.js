import PrjSelector from "/ibfbase/components/prj_selector.js"

const EMPTY_IN={cmt:'',price:'',num:'',sku:'',prj:{value:-1,label:''}};
const RT_TAB="storage_tab";

export default {
components:{
    "prj-select":PrjSelector
},
inject:['service', 'tags', 'ibf'],
data() {return {
    res:[], //工厂中的资产清单
    outlogs:[],
    
    //直接入库
    resCtrl:{cur:1,max:0,inDlg:false,prj:{},
        in:{}, order:'', ordIcon:'swap_vert'},
    olCtrl:{cur:1,max:0}, //出厂日志
    unattach:{no:'',user:[],cmt:'',dlg:false},
    check:{dlg:false,no:'',state:''},
    
    factory:{opts:[],cur:-1,name:''},//工厂选项
    purchase:{},
    sku:{},
    tab:'' //res,gdn,grn,out
}},
created(){
    this.service.myFactories().then(ll=>{
        if(ll.length==0) return;
        this.factory.opts=ll;
        this.factory.cur=ll[0].id;
        this.factory.name=ll[0].name;
        
        this.tab=this.ibf.getRt(RT_TAB, 'res');
        this.tab_changed(this.tab);
    });
},
methods:{
query_res(pg) {
    var offset=(parseInt(pg)-1)*this.service.N_PAGE;
    var opts={method:"GET", url:"/resource/listByFac?factory="
        +this.factory.cur+"&order="+this.resCtrl.order
        +"&num="+this.service.N_PAGE+"&offset="+offset}
    request(opts, this.service.name).then(resp => {
        if(resp.code!=RetCode.OK) {
            this.res=[];
            this.resCtrl.max=0;
            this.resCtrl.cur=1;
            return;
        }
        var dt=new Date();
        for(var l of resp.data.list) {
            dt.setTime(l.inDate*60000);
            l.inDate=datetime2str(dt);
            dt.setTime(l.checkAt*60000);
            l.checkAt=datetime2str(dt);
        }
        this.res = resp.data.list;
        this.resCtrl.max=Math.ceil(resp.data.total/this.service.N_PAGE);
    })
},
query_outlog(pg) {
    var offset=(parseInt(pg)-1)*this.service.N_PAGE;
    var opts={method:"GET", url:"/resource/outlog?factory="
        +this.factory.cur+"&num="+this.service.N_PAGE+"&offset="+offset}
    request(opts, this.service.name).then(resp => {
        if(resp.code!=RetCode.OK) {
            this.outlogs=[];
            this.olCtrl.max=0;
            this.olCtrl.cur=1;
            return;
        }
        var dt=new Date();
        for(var l of resp.data.list) {
            dt.setTime(l.createAt);
            l.createAt=datetime2str(dt);
            l.type=this.tags.outType[l.type];
        }
        this.outlogs=resp.data.list;
        this.olCtrl.max=Math.ceil(resp.data.total/this.service.N_PAGE);
    })
},
tab_changed(tab) {
    this.ibf.setRt(RT_TAB, tab);
    if(tab=='res') {
        if(this.res.length==0) {
            this.query_res(this.resCtrl.cur);
        }
    } else if(tab=='out'){
        if(this.outlogs.length==0) {
            this.query_outlog(this.olCtrl.cur);
        }
    }
},
factory_changed(i) {
    if(i==this.factory.cur)return;
    this.res=[];
    this.grns=[];
    this.gdns=[];
    this.factory.cur=i;
    this.factory.name=this.factory.opts[i].name;
    this.tab_changed(this.tab);
},
changed_res_ord() {
    if(this.resCtrl.order=='') {
        this.resCtrl.order='asc';
        this.resCtrl.ordIcon='vertical_align_top';
    } else if(this.resCtrl.order=='asc') {
        this.resCtrl.order='desc';
        this.resCtrl.ordIcon='vertical_align_bottom';
    } else {
        this.resCtrl.order='';
        this.resCtrl.ordIcon='swap_vert';
    }
    this.query_res(this.resCtrl.cur);
},
show_dir_in() {
    this.resCtrl.tag=this.tags.storage.dir_in;
    copyObjTo(EMPTY_IN, this.resCtrl.in);
    this.resCtrl.inDlg=true;
},
dir_in_do() {
    this.resCtrl.in.sku=this.sku.id;
    var dta=copyObj(this.resCtrl.in, ["num","price","cmt","sku"]);
    if(this.sku.type!='CUR_INVT') { //非零件只能一次入库一个
        dta.num=1;
    }
    dta.factory=this.factory.cur;
    dta.pid=this.resCtrl.prj.id;
    request({method:"POST",url:"/grn/dir_in",data:dta}, this.service.name).then(resp => {
        if(resp.code!=RetCode.OK) {
            this.$refs.errMsg.showErr(resp.code, resp.info);
            return;
        }
        this.resCtrl.inDlg=false;
        this.query_res(this.resCtrl.cur);
    });
},
show_unattach() {
    this.unattach.no='';
    this.unattach.user=[];
    this.unattach.cmt='';
    this.unattach.dlg=true;
},
start_scan() { //开始扫描二维码
    var jsCbId=__regsiterCallback(resp => {
        if(resp.code!=RetCode.OK) {
            this.$refs.alertDlg.showErr(resp.code, resp.info);
            return;
        }
        this.check.no=resp.data.value;
    });
    Platform.scanCode(jsCbId);
},
unattach_do() {
    var opts={method:"POST",url:"/resource/unattach",data:{
        no:this.unattach.no,
        uid:this.unattach.user[0],
        cmt:this.unattach.cmt,
        factory:this.factory.cur
    }};
    request(opts, this.service.name).then(resp => {
        if(resp.code!=RetCode.OK) {
            this.$refs.errMsg.showErr(resp.code, resp.info);
            return;
        }
        this.unattach.dlg=false;
        this.query_res(this.resCtrl.cur);
    });
},
check_res(bad) { //资产清点
    if(!this.check.no)return;
    
    var opts={method:"PUT",url:"/resource/check",data:{
        bad:bad,no:this.check.no,factory:this.factory.cur
    }};
    request(opts, this.service.name).then(resp => {
        if(resp.code!=RetCode.OK) {
            this.$refs.errMsg.showErr(resp.code, resp.info);
        }
    })
}
},
template:`
<q-layout view="hHh lpr fFf">
  <q-header>
   <q-toolbar>
     <q-btn flat icon="arrow_back" dense @click="service.back()"></q-btn>
     <q-toolbar-title>{{tags.storage.title}}</q-toolbar-title>
     <q-btn flat dense icon="factory" :label="factory.name">
       <q-menu>
        <q-list style="min-width:100px">
         <q-item clickable v-close-popup v-for="(f,i) in factory.opts" @click="factory_changed(i)">
           <q-item-section>{{f.name}}</q-item-section>
         </q-item>
        </q-list>
       </q-menu>
     </q-btn>
   </q-toolbar>
  </q-header>
  <q-footer>
   <q-tabs v-model="tab" @update:model-value="tab_changed"
    dense align="justify" switch-indicator inline-label
    class="text-grey bg-grey-3" active-color="primary" indicator-color="primary">
    <q-tab name="res" icon="list" :label="tags.storage.list"></q-tab>
    <q-tab name="out" icon="bus_alert" :label="tags.storage.out_log"></q-tab>
   </q-tabs>
  </q-footer>
  <q-page-container>
    <q-page class="q-pa-none">
<q-tab-panels v-model="tab">

<q-tab-panel name="res" class="q-pa-none">
 <div class="text-right bg-grey-3 q-pa-sm">
  <q-btn color="accent" icon="link_off" @click="show_unattach"
  :label="tags.storage.unattach" flat dense></q-btn>
  <q-btn color="secondary" icon="rule" @click="check.dlg=true"
   :label="tags.storage.check" flat dense></q-btn>
  <q-btn color="primary" @click="show_dir_in"
  :label="tags.storage.dir_in" icon="login" flat dense></q-btn>
 </div>
 <div class="q-pa-sm flex flex-center" v-show="resCtrl.max>1">
  <q-pagination v-model="resCtrl.cur" color="primary" :max="resCtrl.max" max-pages="10"
   boundary-numbers="false" @update:model-value="query_res"></q-pagination>
 </div>
 <q-list dense separator>
  <q-item>
   <q-item-section><q-item-label caption>{{tags.storage.no}}</q-item-label></q-item-section>
   <q-item-section>
    <q-item-label caption>
    {{tags.storage.checkAt}}
    <q-icon :name="resCtrl.ordIcon" @click="changed_res_ord" size="1.5em" color="primary"></q-icon>
    </q-item-label>
   </q-item-section>
   <q-item-section side><q-item-label caption>{{tags.storage.inDate}}</q-item-label></q-item-section>
  </q-item>
  <q-item v-for="(r,i) in res" clickable
   @click="service.goto('/resdetail?no='+r.no+'&factory='+this.factory.cur)">
    <q-item-section>
     <q-item-label>{{r.no}}</q-item-label>
     <q-item-label caption>{{r.skuName}}/{{r.num}}</q-item-label>
    </q-item-section>
    <q-item-section>{{r.checkAt}}</q-item-section>
    <q-item-section side>{{r.inDate}}</q-item-section>
  </q-item>
 </q-list>
</q-tab-panel>

<q-tab-panel name="out" class="q-pa-none">
 <div class="q-pa-sm flex flex-center" v-show="olCtrl.max>1">
  <q-pagination v-model="olCtrl.cur" color="primary" :max="olCtrl.max" max-pages="10"
   boundary-numbers="false" @update:model-value="query_outlog"></q-pagination>
 </div>
 <q-list dense separator class="q-pa-sm">
  <q-item>
   <q-item-section><q-item-label caption>{{tags.storage.no}}</q-item-label></q-item-section>
   <q-item-section><q-item-label caption>{{tags.cmt}}</q-item-label></q-item-section>
   <q-item-section side><q-item-label caption>{{tags.createAt}}</q-item-label></q-item-section>
  </q-item>
  <q-item v-for="(o,i) in outlogs">
    <q-item-section>
     <q-item-label>{{o.no}}</q-item-label>
     <q-item-label caption>{{o.skuName}}/{{o.num}}</q-item-label>
    </q-item-section>
    <q-item-section>
     <q-item-label>{{o.type}}</q-item-label>
     <q-item-label caption>{{o.cmt}}</q-item-label>
    </q-item-section>
    <q-item-section side>
     <q-item-label>{{o.execAcc}}</q-item-label>
     <q-item-label caption>{{o.createAt}}</q-item-label>
    </q-item-section>
  </q-item>
 </q-list>
</q-tab-panel>

</q-tab-panels>

    </q-page>
  </q-page-container>
</q-layout>

<q-dialog v-model="resCtrl.inDlg" persistent><!-- 直接入库 -->
 <q-card style="min-width:70vw">
  <q-card-section>
    <div class="text-h6">{{resCtrl.tag}}</div>
  </q-card-section>
  <q-card-section class="q-pt-none">
   <prj-select v-model="resCtrl.prj" :label="tags.prjName"></prj-select>
   <sku-select v-model="sku" :label="tags.sku.title"></sku-select>
   <q-input v-model.number="resCtrl.in.price" :label="tags.sku.price" dense type="number"></q-input>
   <q-input v-model.number="resCtrl.in.num" :label="tags.num" :disable="sku.type!='CUR_INVT'" type="number"></q-input>
   <q-input v-model="resCtrl.in.cmt" :label="tags.cmt"></q-input>
  </q-card-section>
  <q-card-actions align="right">
   <q-btn :label="tags.ok" color="primary" @click="dir_in_do"></q-btn>
   <q-btn :label="tags.close" color="primary" v-close-popup flat></q-btn>
  </q-card-actions>
 </q-card>
</q-dialog>

<q-dialog v-model="unattach.dlg">
 <q-card style="min-width:70vw">
  <q-card-section>
    <div class="text-h6">{{tags.storage.unattach}}</div>
  </q-card-section>
  <q-card-section class="q-pt-none">
   <q-input v-model="unattach.no" :label="tags.storage.no" dense></q-input>
   <user-selector :accounts="unattach.user" :label="tags.account" :useid="true" :multi="false"></user-selector>
   <q-input v-model="unattach.cmt" :label="tags.cmt" dense></q-input>
  </q-card-section>
  <q-card-actions align="right">
   <q-btn :label="tags.ok" color="primary" @click="unattach_do"></q-btn>
   <q-btn :label="tags.close" color="primary" v-close-popup flat></q-btn>
  </q-card-actions>
 </q-card>
</q-dialog>

<q-dialog v-model="check.dlg">
 <q-card style="min-width:70vw">
  <q-card-section class="row items-center q-pb-none">
   <div class="text-h6">{{tags.storage.check}}</div>
   <q-space></q-space>
   <q-btn icon="close" flat dense v-close-popup></q-btn>
  </q-card-section>
  <q-separator></q-separator>
  <q-card-section class="q-pt-none">
   <q-input v-model="check.no" :label="tags.storage.no" dense>
    <template v-slot:after>
     <q-icon name="qr_code_scanner" @click="start_scan" color="primary"></q-icon>
    </template>
   </q-input>
   <div class="q-gutter-sm">
    <q-btn @click="check_res(true)" :label="tags.storage.chkOk" flat dense color="primary"></q-btn>
    <q-btn @click="check_res(false)" :label="tags.storage.chkBad" flat dense color="accent"></q-btn>
   </div> 
  </q-card-section>
 </q-card>
</q-dialog>

<alert-dialog :title="tags.failToCall" :errMsgs="tags.errMsgs" ref="errMsg"></alert-dialog>
`
}