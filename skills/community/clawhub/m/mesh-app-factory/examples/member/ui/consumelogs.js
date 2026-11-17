export default {
inject:['service', 'tags'],
data() {return {
    orderId:this.$route.query.orderId,
    logs:[],
    pkgName:'',
    vipName:'',
    creatorName:'',
    dlgs:{detail:false, dl:false},
    dlList:[],
    logDetail:{id:0,creator:0,createAt:'',val:0,comment:''}
}},
created(){
    var url="/api/order/getNames?id="+this.orderId;
    request({method:"GET",url:url}, this.service.name).then(resp=>{
        if(resp.code != RetCode.OK) {
            this.$refs.errMsg.showErr(resp.code, resp.info);
            return;
        }
        this.pkgName=resp.data.pkgName;
        this.vipName=resp.data.vipName;
    })
},

methods:{
query_logs(offset,done) {
    var start=(offset-1)*this.service.NUM_PER_PAGE;
    var url="/api/consume/list?offset="+start+"&num="+this.service.NUM_PER_PAGE+"&order="+this.orderId;
    request({method:"GET",url:url}, this.service.name).then(resp=>{
        if(resp.code!=RetCode.OK || !('data' in resp)
           || !('logs' in resp.data) || resp.data.logs.length==0) {
            done(true);
            return;
        }
        this.logs=this.logs.concat(resp.data.logs);
        done(resp.data.logs.length<this.service.NUM_PER_PAGE);
    })
},
detail(i){
    this.dlgs.detail=true;
    this.logDetail=this.logs[i];
},
set_comment(){
    var url="/api/consume/setComment";
    var req={id:this.logDetail.id,comment:this.logDetail.comment};
    request({method:"POST",url:url,data:req}, this.service.name).then(resp=>{
        if(resp.code != 0) {
            this.$refs.errMsg.showErr(resp.code, resp.info);
            return;
        }
        this.dlgs.detail=false;
    })
},
on_load_logs(offset,done){
    this.query_logs(offset,done);
},
dldocx(){
    var fn=this.vipName+'.docx';
    var dlUrl='/api/consume/todocx?order=' + this.orderId;
    download({url:dlUrl, file_name:fn}, this.service.name).then(resp => {
        if(resp.code == RetCode.OK) {
            this.dlList.splice(0,0,{file:resp.data.saveAs, size:resp.data.size, bg:'#00000000'})
        } else {
            this.dlList.splice(0,0,{file:fn, size:0, bg:'#884444'})
        }
        this.dlgs.dl=true;
    })
}
},

template:`
<q-layout view="hHh lpr fFf">
  <q-header class="bg-grey-1 text-primary" elevated>
   <q-toolbar>
      <q-btn flat round icon="arrow_back" dense @click="service.go_back"></q-btn>
      <q-toolbar-title>{{vipName}}-{{pkgName}}</q-toolbar-title>
   </q-toolbar>
  </q-header>

  <q-page-container>
   <q-page class="q-pa-md">
<div id="logs_scroll_area">
 <q-infinite-scroll @load="on_load_logs" :offset="250" scroll-target="#logs_scroll_area">
  <q-markup-table flat>
   <thead><tr>
    <th class="text-left">{{tags.createAt}}</th>
    <th class="text-right">{{tags.comment}}</th>
    <th></th>
   </tr></thead>
   <tbody>
   <tr v-for="(l,i) in logs">
    <td class="text-left">
     <list dense><q-item-section>
      <q-item-label>{{l.createAt}}</q-item-label>
      <q-item-label caption>{{tags.payment}}:{{l.val}}, {{tags.balance}}:{{l.balance}}</q-item-label>
     </q-item-section></list>
    </td>
    <td class="text-right">{{l.comment}}</td>
    <td class="text-right"><q-icon name="edit" @click="detail(i)" color="primary"></q-icon></td>
   </tr>
   </tbody>
  </q-markup-table>
  <template v-slot:loading>
    <div class="row justify-center q-my-md">
      <q-spinner-dots color="primary" size="40px"></q-spinner-dots>
    </div>
  </template>
 </q-infinite-scroll>
</div><!-- end of #logs_scroll_area -->
<q-page-sticky position="bottom-right" :offset="[18,18]">
  <q-btn round color="accent" @click="dldocx" icon="svguse:/assets/imgs/meshicons.svg#word"></q-btn>
</q-page-sticky>
    </q-page>
  </q-page-container>
</q-layout>

<q-dialog v-model="dlgs.detail">
 <q-card style="min-width:70vw">
  <q-card-section>
      <div class="text-h6">{{tags.detailInfo}}</div>
  </q-card-section>
  <q-card-section class="q-pt-none">
   <q-list>
    <q-item>
     <q-item-section>{{tags.creator}}</q-item-section>
     <q-item-section>{{logDetail.creator}}</q-item-section>
    </q-item>
    <q-item>
     <q-item-section>{{tags.createAt}}</q-item-section>
     <q-item-section>{{logDetail.createAt}}</q-item-section>
    </q-item>
    <q-item>
     <q-item-section>{{tags.consumeVal}}</q-item-section>
     <q-item-section>{{logDetail.val}}</q-item-section>
    </q-item>
    <q-item>
     <q-item-section>{{tags.comment}}</q-item-section>
     <q-item-section><q-input v-model="logDetail.comment" dense
     type="textarea" autogrow></q-input></q-item-section>
    </q-item>
   </q-list>
  </q-card-section>
  <q-card-actions align="right">
     <q-btn flat :label="tags.ok" color="primary" @click="set_comment"></q-btn>
     <q-btn flat :label="tags.close" color="primary" v-close-popup></q-btn>
  </q-card-actions>
 </q-card>
</q-dialog>

<q-dialog v-model="dlgs.dl">
<q-card style="min-width:60vw;max-width:90vw">
<q-card-section class="row items-center q-pb-none">
  <div class="text-h6">{{tags.dlList}}</div>
  <q-space></q-space>
  <q-btn icon="close" flat round dense v-close-popup></q-btn>
</q-card-section>
<q-card-section>
 <q-markup-table style="width:100%;" flat>
  <tr v-for="l in dlList" :style="{'background-color':l.bg}">
   <td>{{l.file}}</td>
   <td>{{l.size}}</td>
  </tr>
 </q-markup-table>
</q-card-section>
</q-card>
</q-dialog>
<component-alert-dialog :title="tags.failToCall" :errMsgs="tags.errMsgs" ref="errMsg"></component-alert-dialog>
`
}